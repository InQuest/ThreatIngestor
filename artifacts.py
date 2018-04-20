import re
import ipaddress

import iocextract

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

class Artifact(object):
    """Base class"""

    def __init__(self, artifact, source_name, reference_link=None, reference_text=None):
        self.artifact = artifact
        self.source_name = source_name
        self.reference_link = reference_link or ''
        self.reference_text = reference_text or ''

    def match(self, pattern):
        """Return True if regex pattern matches the deobfuscated artifact, else False.

        May be overridden or extended by child classes."""
        regex = re.compile(pattern)
        return True if regex.search(self.__str__()) else False

    def __unicode__(self):
        return unicode(self.artifact)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class URL(Artifact):
    """URL artifact abstraction, unicode-safe"""

    def _match_expression(self, pattern):
        """Process pattern as a condition expression.

        Raises ValueError if not a valid expression, else returns the
        truthiness of the expression.
        """
        NOT = 'not '
        conditions = [c.strip().lower() for c in pattern.split(',')]
        for condition in conditions:
            if condition.lstrip(NOT) not in URL.__dict__:
                raise ValueError('not a condition expression')
            else:
                result = URL.__dict__[condition.lstrip(NOT)](self)
                if condition.startswith(NOT) and result:
                    return False
                elif not condition.startswith(NOT) and not result:
                    return False
        return True

    def match(self, pattern):
        """Filter on some predefined conditions or a regex pattern.

        If pattern can be parsed as one of the conditions below, it returns the
        truthiness of the resulting expression; otherwise it is treated as regex.

        Valid conditions:

        * is_obfuscated
        * is_ipv4
        * is_ipv6
        * is_ip
        * is_domain
        * not {any above condition}
        * {any comma-separated list of above conditions}

        For example:

        * is_obfuscated, not is_ip
        * not is_obfuscated, is_domain
        """
        try:
            return self._match_expression(pattern)
        except ValueError:
            # not a valid condition expression, treat as regex instead
            return super(URL, self).match(pattern)

    def __unicode__(self):
        """Always returns deobfuscated url"""
        return unicode(iocextract.refang_url(self.artifact))

    def is_obfuscated(self):
        """Boolean: is an obfuscated URL"""
        if self.__unicode__() != unicode(self.artifact):
            # don't treat "example.com" as obfuscated
            if self.__unicode__() != u'http://' + unicode(self.artifact):
                return True
        return False

    def is_ipv4(self):
        """Boolean: URL network location is an IPv4 address, not a domain"""
        parsed = urlparse(iocextract.refang_url(self.artifact))

        try:
            ipaddress.IPv4Address(unicode(parsed.netloc.split(':')[0].replace('[', '').replace(']', '').replace(',', '.')))
        except ValueError:
            return False

        return True

    def is_ipv6(self):
        """Boolean: URL network location is an IPv6 address, not a domain"""
        # fix urlparse exception
        parsed = urlparse(iocextract.refang_url(self.artifact))

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
        return urlparse(self.__unicode__()).netloc.split(':')[0]

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


class Hash(Artifact):
    """Hash artifact abstraction"""

    # Types
    MD5 = 'md5'
    SHA1 = 'sha1'
    SHA256 = 'sha256'
    SHA512 = 'sha512'

    def hash_type(self):
        """Return the hash type as a string, or None"""
        if len(self.artifact) == 32:
            return self.MD5
        elif len(self.artifact) == 40:
            return self.SHA1
        elif len(self.artifact) == 64:
            return self.SHA256
        elif len(self.artifact) == 128:
            return self.SHA512
        else:
            return None


class YARASignature(Artifact):
    """YARA signature artifact abstraction"""
    pass


# Define string mappings for artifact types
STRING_MAP = {
    'url': URL,
    'ipaddress': IPAddress,
    'domain': Domain,
    'yarasignature': YARASignature
}
