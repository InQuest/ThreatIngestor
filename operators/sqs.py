from __future__ import absolute_import
import sys
import json

try:
    import boto3
except ImportError:
    sys.stderr.write("warn: dependency boto3 required for SQS operator is not installed\n")

import artifacts
from operators import Operator

class SQS(Operator):
    """Operator for Amazon SQS"""

    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, queue_name, **kwargs):
        """SQS operator"""
        self.sqs = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.queue_url = self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']

        # kwargs are used to dynamically form message body
        self.kwargs = kwargs

        super(SQS, self).__init__(kwargs.get('artifact_types'), kwargs.get('filter_string'), kwargs.get('allowed_sources'))
        self.artifact_types = kwargs.get('artifact_types') or [
            artifacts.URL,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        if isinstance(artifact, artifacts.URL):
            self.handle_url(artifact)

    def handle_url(self, url):
        """Handle a single URL; excludes IP-based URLs"""
        # allow interpolation from kwargs
        message_body = dict([(k, v.format(
            url=unicode(url),
            domain=url.domain()
        )) for (k, v) in self.kwargs.iteritems()])

        self._sqs_put(json.dumps(message_body))

    def _sqs_put(self, content):
        """Send content to an SQS queue"""
        return self.sqs.send_message(
                QueueUrl=self.queue_url,
                DelaySeconds=0,
                MessageBody=content
        )
