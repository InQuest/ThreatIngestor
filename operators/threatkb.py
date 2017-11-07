from __future__ import absolute_import

import threatkb

import artifacts
from operators import Operator

class ThreatKB(Operator):
    """Operator for InQuest ThreatKB"""

    def __init__(self, url, email, password, state):
        """ThreatKB operator"""
        self.state = state
        self.api = threatkb.ThreatKB(url, email, password)

        self.artifact_types = [artifacts.Domain, artifacts.IPAddress, artifacts.YaraSignature]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        if isinstance(artifact, artifacts.Domain):
            self.handle_domain(artifact)
        elif isinstance(artifact, artifacts.IPAddress):
            self.handle_ipaddress(artifact)
        elif isinstance(artifact, artifacts.YaraSignature):
            self.handle_yarasignature(artifact)

    def handle_domain(self, domain):
        """Handle a single domain"""
        existing = self.api.get('c2dns')
        if str(domain) in [dns['domain_name'].encode('utf-8') for dns in existing]:
            # post comment
            self.api.create('comments', {
                    'comment': u"{c}\n\n{u}".format(c=domain.reference_text, u=domain.reference_link),
                    'entity_id': [dns['id'] for dns in existing if dns['domain_name'].encode('utf-8') == str(domain)][:1],
                    'entity_type': 2,
                })
        else:
            # post c2 domain
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
        existing = self.api.get('c2ips')
        if str(ipaddress) in [addr['ip'] for addr in existing]:
            # post comment
            self.api.create('comments', {
                    'comment': u"{c}\n\n{u}".format(c=ipaddress.reference_text, u=ipaddress.reference_link),
                    'entity_id': [addr['id'] for addr in existing if addr['ip'] == str(ipaddress)][0],
                    'entity_type': 3,
                })
        else:
            # post c2 ip
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
        """Handle a single Yara signature"""
        pass
