import re
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

import extractlib

import artifacts


TRUNCATE_LENGTH = 140


class Source:
    """Base class, see method documentation"""

    def __init__(self, name=None):
        """Args should be url, auth, etc, whatever is needed to set up the object."""
        self.name = name
        raise NotImplementedError()

    def run(self, saved_state):
        """Run and return (saved_state, list(Artifact)).

        Attempts to pick up where we left off using saved_state, if supported."""
        raise NotImplementedError()

    def process_element(self, content, reference_link, include_nonobfuscated=False):
        """Take a single source content/url and return a list of Artifacts"""

        # truncate content to a reasonable length for reference_text
        reference_text = content[:TRUNCATE_LENGTH] + ('...' if len(content) > TRUNCATE_LENGTH else '')

        # enable detection of some extra obfuscated urls
        content = content.replace(' [.] ', '[.]')
        matches = re.findall(r'[^/\w.\[\]-]?([\w-]+\[\.\]\w+)[\W\b]?', content)
        for match in set(matches):
            if not ']https' in match:
                # special case for broken tweets
                content = content.replace(match, 'hxxp://{u}'.format(u=match))

        artifact_list = []

        # collect URLs and domains
        scraped = extractlib.extract_info(content, generic_urls=True)
        for url in scraped:
            # dump anything with ellipses, these get through the regex
            if u'\u2026' in url:
                continue

            artifact = artifacts.URL(url, self.name, reference_link=reference_link,
                                     reference_text=reference_text)

            # dump urls that appear to have the same domain as reference_url
            if artifact.domain() == urlparse(reference_link).netloc:
                continue

            if artifact.is_obfuscated() or include_nonobfuscated:
                # do URL collection
                artifact_list.append(artifact)

                # do domain collection in the same pass
                if artifact.is_domain():
                    artifact_list.append(artifacts.Domain(artifact.domain(), self.name,
                                                          reference_link=reference_link,
                                                          reference_text=reference_text))

        # collect IPs
        scraped = extractlib.extract_info(content, ips=True)
        for ip in scraped:
            artifact = artifacts.IPAddress(ip, self.name, reference_link=reference_link,
                                           reference_text=reference_text)

            try:
                if artifact.ipaddress().is_private or artifact.ipaddress().is_loopback:
                    # don't care
                    continue

            except ValueError:
                # invalid IP
                continue

            artifact_list.append(artifact)

        # collect yara rules
        scraped = extractlib.extract_yara_rules(content)
        for rule in scraped:
            artifact = artifacts.YARASignature(rule, self.name, reference_link=reference_link,
                                               reference_text=reference_text)

            artifact_list.append(artifact)

        return artifact_list
