from __future__ import absolute_import

import threatkb

import artifacts
from operators import Operator

class ThreatKB(Operator):
    """Operator for InQuest ThreatKB"""

    def __init__(self, url, email, password, state, artifact_types=None):
        """ThreatKB operator"""
        self.state = state
        self.api = threatkb.ThreatKB(url, email, password)

        self.artifact_types = artifact_types or [
            artifacts.Domain,
            artifacts.IPAddress,
            artifacts.YARASignature,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        if isinstance(artifact, artifacts.Domain):
            self.handle_domain(artifact)
        elif isinstance(artifact, artifacts.IPAddress):
            self.handle_ipaddress(artifact)
        elif isinstance(artifact, artifacts.YARASignature):
            self.handle_yarasignature(artifact)

    def handle_domain(self, domain):
        """Handle a single domain"""
        self.api.create('c2dns', {
                'domain_name': str(domain),
                'match_type': '',
                'reference_link': domain.reference_link,
                'description': domain.reference_text,
                'expiration_type': '',
                'state': {'state': self.state},
                'tags': [],
            })

    def handle_ipaddress(self, ipaddress):
        """Handle a single IP address"""
        self.api.create('c2ips', {
                'ip': str(ipaddress),
                'reference_link': ipaddress.reference_link,
                'description': ipaddress.reference_text,
                'expiration_type': '',
                'state': {'state': self.state},
                'asn': '',
                'country': '',
                'city': '',
                'st': '',
                'tags': [],
            })

    def handle_yarasignature(self, yarasignature):
        """Handle a single YARA signature"""
        self.api.create('import', {
                'autocommit': 1,
                'import_text': str(yarasignature),
                'shared_reference': yarasignature.reference_link,
                'shared_state': {'state': self.state},
            })
