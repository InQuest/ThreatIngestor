from __future__ import absolute_import


import threatingestor.artifacts
from threatingestor.operators import Operator
from threatingestor.exceptions import DependencyError


try:
    import pymisp
except ImportError:
    raise DependencyError("Dependency PyMISP required for MISP operator is not installed")


class Plugin(Operator):
    """Operator for MISP."""
    def __init__(self, url, key, ssl=True, tags=None, artifact_types=None, filter_string=None, allowed_sources=None):
        """MISP operator."""
        self.api = pymisp.PyMISP(url, key, ssl, 'json')
        if tags:
            self.tags = tags
        else:
            self.tags = ['type:OSINT']
        self.event_info = 'ThreatIngestor Event: {source_name}'

        super(Plugin, self).__init__(artifact_types, filter_string, allowed_sources)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
            threatingestor.artifacts.YARASignature,
        ]


    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        if isinstance(artifact, threatingestor.artifacts.Domain):
            self.handle_domain(artifact)
        if isinstance(artifact, threatingestor.artifacts.Hash):
            self.handle_hash(artifact)
        elif isinstance(artifact, threatingestor.artifacts.IPAddress):
            self.handle_ipaddress(artifact)
        if isinstance(artifact, threatingestor.artifacts.URL):
            self.handle_url(artifact)
        elif isinstance(artifact, threatingestor.artifacts.YARASignature):
            self.handle_yarasignature(artifact)


    def _create_event(self, artifact):
        """Create an event in MISP, return an Event object."""
        event = self.api.new_event(info=self.event_info.format(
            source_name=artifact.source_name))

        # Add tags.
        for tag in self.tags:
            self.api.add_tag(event, tag)

        # Add references.
        self.api.add_internal_link(event, artifact.reference_link)
        self.api.add_internal_text(event, artifact.reference_text)
        self.api.add_internal_other(event, f'source:{artifact.source_name}')

        return event


    def handle_domain(self, domain):
        """Handle a single domain."""
        event = self._create_event(domain)
        self.api.add_domain(event, str(domain))

    def handle_hash(self, hash_):
        """Handle a single hash."""
        if hash_.hash_type() == hash_.MD5:
            event = self._create_event(hash_)
            self.api.add_hashes(event, md5=str(hash_))
        elif hash_.hash_type() == hash_.SHA1:
            event = self._create_event(hash_)
            self.api.add_hashes(event, sha1=str(hash_))
        elif hash_.hash_type() == hash_.SHA256:
            event = self._create_event(hash_)
            self.api.add_hashes(event, sha256=str(hash_))


    def handle_ipaddress(self, ipaddress):
        """Handle a single IP address."""
        event = self._create_event(ipaddress)
        self.api.add_ipdst(event, str(ipaddress))


    def handle_url(self, url):
        """Handle a single URL."""
        event = self._create_event(url)
        self.api.add_url(event, str(url))


    def handle_yarasignature(self, yarasignature):
        """Handle a single YARA signature."""
        event = self._create_event(yarasignature)
        self.api.add_yara(event, str(yarasignature))
