import json

from threatingestor.exceptions import DependencyError
from threatingestor.sources import abstract_json

try:
    import greenstalk
except ImportError:
    raise DependencyError("Dependency greenstalk required for Beastalk operator is not installed")

class Plugin(abstract_json.AbstractPlugin):
    """Source for Beanstalk work queue"""

    def __init__(self, name, host, port, queue_name, paths, reference=None)
        """Beanstalk source"""
        super(Plugin, self).__init__(name, paths, reference)
        self.queue = greenstalk.Client(host, port, watch=queue_name)

    def get_objects(self, saved_state):
        # Just do one job at a time, so we don't have to worry about batching
        # or TTL timeouts.
        message = self.queue.reserve()
        job = json.loads(message.body)

        # Let the queue know that the message is processed.
        self.queue.delete(message)

        # Return the job inside a list.
        return saved_state, [job]
