from __future__ import absolute_import


import threatingestor.artifacts
from threatingestor.operators import Operator
from threatingestor.exceptions import DependencyError


try:
    import pymisp
except ImportError:
    raise DependencyError(
        "Dependency PyMISP required for MISP operator is not installed"
    )


class Plugin(Operator):
    """Operator for MISP."""

    def __init__(self, url, key, ssl=True, tags=None, artifact_types=None, filter_string=None, allowed_sources=None):
        """MISP operator."""
        self.api = pymisp.ExpandedPyMISP(url, key, ssl)
        if tags:
            self.tags = tags
        else:
            self.tags = ['type:OSINT']
        self.event_info = 'ThreatIngestor Event: {source_name}'

        super(Plugin, self).__init__(
            artifact_types, filter_string, allowed_sources
        )
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
            threatingestor.artifacts.YARASignature,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        event = self._find_or_create_event(artifact)

        if isinstance(artifact, threatingestor.artifacts.Domain):
            event = self.handle_domain(artifact, event=event)
        if isinstance(artifact, threatingestor.artifacts.Hash):
            event = self.handle_hash(artifact, event=event)
        elif isinstance(artifact, threatingestor.artifacts.IPAddress):
            event = self.handle_ipaddress(artifact, event=event)
        if isinstance(artifact, threatingestor.artifacts.URL):
            event = self.handle_url(artifact, event=event)
        elif isinstance(artifact, threatingestor.artifacts.YARASignature):
            event = self.handle_yarasignature(artifact, event=event)

        self._update_or_create_event(event)

    def _update_or_create_event(self, event):
        """Update or create an event for the artifact."""
        event_dict = event.to_dict()
        attributes = event_dict.get("Attribute", [])
        if not attributes:
            return
        # If an event doesn't have "date" field, it is not created int MISP
        if event_dict.get("date") is None:
            self.api.add_event(event)
        else:
            self.api.update_event(event)

    def _find_or_create_event(self, artifact):
        """Find or create an event for the artifact."""
        event = self._find_event(artifact)
        if event is not None:
            return event

        return self._create_event(artifact)

    def _find_event(self, artifact):
        """Find an event which has the same refetrence link, return an Event object."""
        events = self.api.search(
            "events",
            limit=1,
            type_attribute="link",
            value=artifact.reference_link,
            pythonify=True
        )
        if len(events) == 1:
            return events[0]

        return None

    def _create_event(self, artifact):
        """Create an event in MISP, return an Event object."""
        event = pymisp.MISPEvent()
        event.info = self.event_info.format(source_name=artifact.source_name)

        # Add tags.
        for tag in self.tags:
            event.add_tag(tag)

        # Add references.
        if artifact.reference_link != "":
            event.add_attribute("link", artifact.reference_link)
        if artifact.reference_text != "":
            event.add_attribute("text", artifact.reference_text)
        if artifact.source_name != "":
            event.add_attribute("other",  f'source:{artifact.source_name}')

        return event

    def handle_domain(self, domain, event: pymisp.MISPEvent):
        """Handle a single domain."""
        event.add_attribute("domain", str(domain))
        return event

    def handle_hash(self, hash_, event: pymisp.MISPEvent):
        """Handle a single hash."""
        if hash_.hash_type() == hash_.MD5:
            event.add_attribute("md5", str(hash_))
        elif hash_.hash_type() == hash_.SHA1:
            event.add_attribute("sha1", str(hash_))
        elif hash_.hash_type() == hash_.SHA256:
            event.add_attribute("sha256", str(hash_))
        return event

    def handle_ipaddress(self, ipaddress, event: pymisp.MISPEvent):
        """Handle a single IP address."""
        event.add_attribute("ip-dst", str(ipaddress))
        return event

    def handle_url(self, url, event: pymisp.MISPEvent):
        """Handle a single URL."""
        event.add_attribute("url", str(url))
        return event

    def handle_yarasignature(self, yarasignature, event: pymisp.MISPEvent):
        """Handle a single YARA signature."""
        event.add_attribute("yara", str(yarasignature))
        return event
