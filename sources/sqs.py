from __future__ import absolute_import
import sys
import json

try:
    import boto3
except ImportError:
    sys.stderr.write("warn: dependency boto3 required for SQS source is not installed\n")

import requests

from sources import Source

class SQS(Source):
    """Source for Amazon SQS"""

    def __init__(self, name, aws_access_key_id, aws_secret_access_key, aws_region, queue_name):
        """SQS source"""
        self.name = name
        self.sqs = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

    def run(self, saved_state):

        artifact_list = []
        for message in self.queue.receive_messages():
            # Process a link.
            job = json.loads(message.body)
            response = requests.get(job['link'])
            artifact_list += self.process_element(response.text, job['link'], include_nonobfuscated=True)

            # Let the queue know that the message is processed.
            message.delete()

        return saved_state, artifact_list
