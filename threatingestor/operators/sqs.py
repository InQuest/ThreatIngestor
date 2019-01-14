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

    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, queue_name,
            artifact_types=None, filter_string=None, allowed_sources=None, **kwargs):
        """SQS operator"""
        self.sqs = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.queue_url = self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']

        # kwargs are used to dynamically form message body
        self.kwargs = kwargs

        super(Plugin, self).__init__(artifact_types=artifact_types,
                                     filter_string=filter_string,
                                     allowed_sources=allowed_sources)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.URL,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        message_body = dict([(k, artifact.format_message(v)) for (k, v) in self.kwargs.items()])

        self._sqs_put(json.dumps(message_body))

    def _sqs_put(self, content):
        """Send content to an SQS queue"""
        return self.sqs.send_message(
                QueueUrl=self.queue_url,
                DelaySeconds=0,
                MessageBody=content
        )
