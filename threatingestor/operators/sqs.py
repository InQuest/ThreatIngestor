import json


from threatingestor.exceptions import DependencyError
import threatingestor.artifacts
from threatingestor.operators import abstract_json


try:
    import boto3
except ImportError:
    raise DependencyError("Dependency boto3 required for SQS operator is not installed")


class Plugin(abstract_json.AbstractPlugin):
    """Operator for Amazon SQS."""
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, queue_name,
            artifact_types=None, filter_string=None, allowed_sources=None, **kwargs):
        """SQS operator."""
        self.sqs = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.queue_url = self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']

        super(Plugin, self).__init__(artifact_types=artifact_types,
                                     filter_string=filter_string,
                                     allowed_sources=allowed_sources,
                                     **kwargs)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.URL,
        ]


    def _put(self, content):
        """Send content to an SQS queue."""
        return self.sqs.send_message(
                QueueUrl=self.queue_url,
                DelaySeconds=0,
                MessageBody=json.dumps(content)
        )
