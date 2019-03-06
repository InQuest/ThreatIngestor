import json


from threatingestor.exceptions import DependencyError
from threatingestor.sources import abstract_json


try:
    import boto3
except ImportError:
    raise DependencyError("Dependency boto3 required for SQS operator is not installed")


class Plugin(abstract_json.AbstractPlugin):
    """Source for Amazon SQS."""
    def __init__(self, name, aws_access_key_id, aws_secret_access_key,
            aws_region, queue_name, paths, reference=None):
        """SQS source."""
        super(Plugin, self).__init__(name, paths, reference)
        self.sqs = boto3.resource('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)


    def get_objects(self, saved_state):
        content_list = []
        for message in self.queue.receive_messages():
            # Process a message.
            job = json.loads(message.body)
            content_list.append(job)

            # Let the queue know that the message is processed.
            message.delete()

        return saved_state, content_list
