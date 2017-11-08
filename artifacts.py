import urlparse
import ipaddress

class Artifact:
    """Base class"""

    def __init__(self, artifact, reference_link, reference_text=None):
        self.artifact = artifact
        self.reference_link = reference_link
        self.reference_text = reference_text or ''

    def __unicode__(self):
        return unicode(self.artifact)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class URL(Artifact):
    """URL artifact abstraction, unicode-safe"""

    def _get_clean_url(self):
        """Fixes urlparse errors"""
        url = self.artifact

        # fix ipv6 parsing exception
        if '[.' in url and '[.]' not in url:
            url = url.replace('[.', '[.]')
        if '.]' in url and '[.]' not in url:
            url = url.replace('.]', '[.]')
        if '[/]' in url:
            url = url.replace('[/]', '/')
        if '[' in url and ']' not in url:
            url = url.replace('[', '')

        try:
            urlparse.urlparse(url)
        except ValueError:
            # last resort on ipv6 fail
            url = url.replace('[', '').replace(']', '')
            urlparse.urlparse(url)

        # urlparse expects a scheme, make sure one exists
        if '//' not in url:
            url = 'http://' + url

        return url

    def __unicode__(self):
        """Always returns deobfuscated url"""
        url = self._get_clean_url()

        parsed = urlparse.urlparse(url)

        # Handle URLs with no scheme / obfuscated scheme
        # Note: ParseResult._replace is a public member, this is safe
        if parsed.scheme not in ['http', 'https', 'ftp']:
            parsed = parsed._replace(scheme='http')
            url = parsed.geturl().replace('http:///', 'http://')
            parsed = urlparse.urlparse(url)

        # Fix example[.]com, but keep RFC 2732 URLs intact
        if not self.is_ipv6():
            parsed = parsed._replace(netloc=parsed.netloc.replace('[dot]', '[.]').replace('[', '').\
                                                   replace(']', '').replace('(', '').replace(')', '').\
                                                   replace(',', '.').split()[0])

        # fix unicode obfuscation
        if u'\u30fb' in parsed.netloc:
            parsed = parsed._replace(netloc=parsed.netloc.replace(u'\u30fb', '.'))

        return unicode(parsed.geturl())

    def is_obfuscated(self):
        """Boolean: is an obfuscated URL"""
        return self.__unicode__() != unicode(self._get_clean_url())

    def is_ipv4(self):
        """Boolean: URL network location is an IPv4 address, not a domain"""
        parsed = urlparse.urlparse(self._get_clean_url())

        try:
            ipaddress.IPv4Address(unicode(parsed.netloc.split(':')[0].replace('[', '').replace(']', '').replace(',', '.')))
        except ValueError:
            return False

        return True

    def is_ipv6(self):
        """Boolean: URL network location is an IPv6 address, not a domain"""
        # fix urlparse exception
        parsed = urlparse.urlparse(self._get_clean_url())

        # Handle RFC 2732 IPv6 URLs with and without port, as well as non-RFC IPv6 URLs
        if ']:' in parsed.netloc:
            ipv6 = ':'.join(parsed.netloc.split(':')[:-1])
        else:
            ipv6 = parsed.netloc

        try:
            ipaddress.IPv6Address(unicode(ipv6.replace('[', '').replace(']', '')))
        except ValueError:
            return False

        return True

    def is_ip(self):
        """Boolean: URL network location is an IP address, not a domain"""
        return self.is_ipv4() or self.is_ipv6()

    def domain(self):
        """Deobfuscated domain; undefined behavior if self.is_ip()"""
        return urlparse.urlparse(self.__unicode__()).netloc.split(':')[0]

    def is_domain(self):
        """Boolean: URL network location might be a valid domain"""
        return not self.is_ip() and len(self.domain()) > 3 and '.' in self.domain()[1:-1] and \
               all([str.isalnum(x.encode('utf-8')) or x in '-.' for x in self.domain()]) and \
               self.domain()[self.domain().rfind('.')+1:].isalpha() and len(self.domain()[self.domain().rfind('.')+1:]) > 1

    def deobfuscated(self):
        """Named method for clarity, same as unicode(my_url_object)"""
        return self.__unicode__()


class IPAddress(Artifact):
    """IP address artifact abstraction

    Use version and ipaddress() for processing."""

    def __unicode__(self):
        """Always returns deobfuscated IP"""
        return unicode(self.artifact.replace('[', '').replace(']', '').split('/')[0].split(':')[0].split(' ')[0])

    @property
    def version(self):
        """Returns 4, 6, or None"""
        try:
            return ipaddress.IPv4Address(self.__unicode__()).version
        except ValueError:
            try:
                return ipaddress.IPv6Address(self.__unicode__()).version
            except ValueError:
                return None

    def ipaddress(self):
        """Return ipaddress.IPv4Address or ipaddress.IPv6Address object, or raise ValueError"""
        version = self.version
        if version == 4:
            return ipaddress.IPv4Address(self.__unicode__())
        elif version == 6:
            return ipaddress.IPv6Address(self.__unicode__())
        else:
            raise ValueError(u"Invalid IP address '{ip}'".format(ip=self.artifact))


class Domain(Artifact):
    """Domain artifact abstraction"""
    pass


class YARASignature(Artifact):
    """YARA signature artifact abstraction"""
    pass
