import re
from urllib.parse import urlparse
import itertools


import iocextract
from loguru import logger


import threatingestor.artifacts


TRUNCATE_LENGTH = 140


class Source:
    """Base class for all Source plugins.

    Note: This is an abstract class. You must override ``__init__`` and ``run``
    in child classes. You should not override ``process_element``. When adding
    additional methods to child classes, consider prefixing the method name
    with an underscore to denote a ``_private_method``.
    """
    def __init__(self, name, *args, **kwargs):
        """Override this constructor in child classes.

        The first argument must always be ``name``.

        Other argumentss should be url, auth, etc, whatever is needed to set
        up the object.
        """
        raise NotImplementedError()


    def run(self, saved_state):
        """Run and return ``(saved_state, list(Artifact))``.

        Override this method in child classes.

        The method signature and return values must remain consistent.

        The method should attempt to pick up where we left off using
        ``saved_state``, if supported. If ``saved_state`` is ``None``, you can
        assume this is a first run. If state is maintained by the remote
        resource (e.g. as it is with SQS), ``saved_state`` should always be
        ``None``.
        """
        raise NotImplementedError()


    def process_element(self, content, reference_link, include_nonobfuscated=False):
        """Take a single source content/url and return a list of Artifacts.

        This is the main work block of Source plugins, which handles
        IOC extraction and artifact creation.

        :param content: String content to extract from.
        :param reference_link: Reference link to attach to all artifacts.
        :param include_nonobfuscated: Include non-defanged URLs in output?
        """
        logger.debug(f"Processing in source '{self.name}'")

        # Truncate content to a reasonable length for reference_text.
        reference_text = content[:TRUNCATE_LENGTH] + ('...' if len(content) > TRUNCATE_LENGTH else '')

        # Initialize an empty list and a map of counters to track each artifact type.
        artifact_list = []
        artifact_type_count = {
            'domain': 0,
            'hash': 0,
            'ipaddress': 0,
            'task': 0,
            'url': 0,
            'yarasignature': 0,
        }

        # Collect URLs and domains.
        scraped = itertools.chain(
            iocextract.extract_unencoded_urls(content),
            # Decode encoded URLs, since we can't operate on encoded ones.
            iocextract.extract_encoded_urls(content, refang=True),
        )
        for url in scraped:
            # Dump anything with ellipses, these get through the regex.
            if u'\u2026' in url:
                continue

            artifact = threatingestor.artifacts.URL(url, self.name,
                                                    reference_link=reference_link,
                                                    reference_text=reference_text)

            # Dump URLs that appear to have the same domain as reference_url.
            try:
                if artifact.domain() == urlparse(reference_link).netloc:
                    continue
            except ValueError:
                # Error parsing reference_link as a URL. Ignoring.
                pass

            if artifact.is_obfuscated() or include_nonobfuscated:
                # Do URL collection.
                artifact_list.append(artifact)
                artifact_type_count['url'] += 1

                # Do domain collection in the same pass.
                # Note: domains will always be a subset of URLs. There is no
                # domain extraction.
                if artifact.is_domain():
                    artifact_list.append(
                            threatingestor.artifacts.Domain(artifact.domain(), self.name,
                                                            reference_link=reference_link,
                                                            reference_text=reference_text))
                    artifact_type_count['domain'] += 1

        # Collect IPs.
        scraped = iocextract.extract_ips(content)
        for ip in scraped:
            artifact = threatingestor.artifacts.IPAddress(ip, self.name,
                                                          reference_link=reference_link,
                                                          reference_text=reference_text)

            try:
                ipaddress = artifact.ipaddress()
                if ipaddress.is_private or ipaddress.is_loopback or ipaddress.is_reserved:
                    # Skip private, loopback, reserved IPs.
                    continue

            except ValueError:
                # Skip invalid IPs.
                continue

            artifact_list.append(artifact)
            artifact_type_count['ipaddress'] += 1

        # Collect YARA rules.
        scraped = iocextract.extract_yara_rules(content)
        for rule in scraped:
            artifact = threatingestor.artifacts.YARASignature(rule, self.name,
                                                              reference_link=reference_link,
                                                              reference_text=reference_text)

            artifact_list.append(artifact)
            artifact_type_count['yarasignature'] += 1

        # Collect hashes.
        scraped = iocextract.extract_hashes(content)
        for hash_ in scraped:
            artifact = threatingestor.artifacts.Hash(hash_, self.name,
                                                     reference_link=reference_link,
                                                     reference_text=reference_text)

            artifact_list.append(artifact)
            artifact_type_count['hash'] += 1

        # Generate generic task.
        title = f"Manual Task: {reference_link}"
        description = f"URL: {reference_link}\nTask autogenerated by ThreatIngestor from source: {self.name}"
        artifact = threatingestor.artifacts.Task(title, self.name,
                                                 reference_link=reference_link,
                                                 reference_text=description)
        artifact_list.append(artifact)
        artifact_type_count['task'] += 1

        logger.debug(f"Found {len(artifact_list)} total artifacts")
        logger.debug(f"Type breakdown: {artifact_type_count}")
        return artifact_list
