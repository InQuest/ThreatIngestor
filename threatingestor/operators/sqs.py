import sys
import json

from threatingestor.exceptions import DependencyError
from threatingestor.operators import Operator
import threatingestor.artifacts

try:
    import boto3
except ImportError:
    raise DependencyError("Dependency boto3 required for SQS operator is not installed")

class Plugin(Operator):
    """Operator for Amazon SQS"""

    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, queue_name, **kwargs):
        """SQS operator"""
        self.sqs = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.queue_url = self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']

        # kwargs are used to dynamically form message body
        self.kwargs = kwargs

        super(Plugin, self).__init__(kwargs.get('artifact_types'), kwargs.get('filter_string'), kwargs.get('allowed_sources'))
        self.artifact_types = kwargs.get('artifact_types') or [
            threatingestor.artifacts.URL,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        format_fn = None
        if isinstance(artifact, threatingestor.artifacts.URL):
            format_fn = _format_value_url
        elif isinstance(artifact, threatingestor.artifacts.Hash):
            format_fn = _format_value_hash
        elif isinstance(artifact, threatingestor.artifacts.IPAddress):
            format_fn = _format_value_ipaddress
        elif isinstance(artifact, threatingestor.artifacts.Domain):
            format_fn = _format_value_domain
        elif isinstance(artifact, threatingestor.artifacts.YARASignature):
            format_fn = _format_value_yarasignature

        if format_fn:
            # it's an artifact type we know how to handle
            message_body = dict([(k, format_fn(v, artifact)) for (k, v) in self.kwargs.iteritems()])

            self._sqs_put(json.dumps(message_body))

    def _sqs_put(self, content):
        """Send content to an SQS queue"""
        return self.sqs.send_message(
                QueueUrl=self.queue_url,
                DelaySeconds=0,
                MessageBody=content
        )

def _format_value_url(value, url):
    """Allow interpolation from kwargs"""
    return value.format(
        url=unicode(url),
        domain=url.domain()
    )

def _format_value_domain(value, domain):
    """Allow interpolation from kwargs"""
    return value.format(
        domain=unicode(domain)
    )

def _format_value_ipaddress(value, ipaddress):
    """Allow interpolation from kwargs"""
    return value.format(
        ipaddress=unicode(ipaddress)
    )

def _format_value_hash(value, hash_):
    """Allow interpolation from kwargs"""
    return value.format(
        hash=unicode(hash_)
    )

def _format_value_yarasignature(value, yarasignature):
    """Allow interpolation from kwargs"""
    return value.format(
        yarasignature=unicode(yarasignature)
    )
