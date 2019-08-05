from __future__ import absolute_import


import threatingestor.artifacts
from threatingestor.operators import Operator
from threatingestor.exceptions import DependencyError


try:
    import threatkb
except ImportError:
    raise DependencyError("Dependency threatkb required for ThreatKB operator is not installed")


class Plugin(Operator):
    """Operator for InQuest ThreatKB."""
    def __init__(self, url, token, secret_key, state, artifact_types=None, filter_string=None, allowed_sources=None, use_https=False):
        """ThreatKB operator."""
        self.state = state
        self.api = threatkb.ThreatKB(url, token, secret_key, use_https=use_https)

        super(Plugin, self).__init__(artifact_types, filter_string, allowed_sources)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.YARASignature,
        ]


    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        if isinstance(artifact, threatingestor.artifacts.Domain):
            self.handle_domain(artifact)
        elif isinstance(artifact, threatingestor.artifacts.IPAddress):
            self.handle_ipaddress(artifact)
        elif isinstance(artifact, threatingestor.artifacts.YARASignature):
            self.handle_yarasignature(artifact)
        elif isinstance(artifact, threatingestor.artifacts.Task):
            self.handle_task(artifact)


    def handle_domain(self, domain):
        """Handle a single domain."""
        self.api.create('c2dns', {
                'domain_name': str(domain),
                'match_type': '',
                'description': '{l}\n\n{t}'.format(l=domain.reference_link, t=domain.reference_text),
                'references': '',
                'expiration_type': '',
                'state': {'state': self.state},
                'tags': [],
                'metadata_values': {},
            })


    def handle_ipaddress(self, ipaddress):
        """Handle a single IP address."""
        self.api.create('c2ips', {
                'ip': str(ipaddress),
                'references': '',
                'description': '{l}\n\n{t}'.format(l=ipaddress.reference_link, t=ipaddress.reference_text),
                'expiration_type': '',
                'state': {'state': self.state},
                'asn': '',
                'country': '',
                'city': '',
                'st': '',
                'tags': [],
                'metadata_values': {},
            })


    def handle_yarasignature(self, yarasignature):
        """Handle a single YARA signature."""
        self.api.create('import', {
                'autocommit': 1,
                'import_text': str(yarasignature),
                'shared_reference': yarasignature.reference_link,
                'shared_state': self.state,
                'extract_ip': False,
                'extract_dns': False,
            })


    def handle_task(self, task):
        """Handle a single Task."""
        self.api.create('tasks', {
                'title': str(task),
                'description': task.reference_text,
                'state': {'state': self.state},
                'final_artifact': '',
            })
