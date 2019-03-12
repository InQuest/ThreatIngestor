import json


from threatingestor.exceptions import DependencyError
from threatingestor.sources import abstract_json


try:
    import greenstalk
except ImportError:
    raise DependencyError("Dependency greenstalk required for Beastalk operator is not installed")


BATCH_SIZE = 10


class Plugin(abstract_json.AbstractPlugin):
    """Source for Beanstalk work queue."""
    def __init__(self, name, host, port, queue_name, paths, reference=None):
        """Beanstalk source."""
        super(Plugin, self).__init__(name, paths, reference)
        self.queue = greenstalk.Client(host, port, watch=queue_name)


    def get_objects(self, saved_state):
        job_list = []

        # Just do one job at a time, so we don't have to worry about batching
        # or TTL timeouts.
        try:
            batch_count = 0
            while batch_count < BATCH_SIZE:
                message = self.queue.reserve(timeout=1)
                job = json.loads(message.body)
                job_list.append(job)

                # Let the queue know that the message is processed.
                self.queue.delete(message)
                batch_count += 1

        except greenstalk.TimedOutError:
            # No more jobs.
            pass

        # Return the job list.
        return saved_state, job_list
