import json


from threatingestor.exceptions import DependencyError
import threatingestor.artifacts
from threatingestor.operators import abstract_json


try:
    import greenstalk
except ImportError:
    raise DependencyError("Dependency greenstalk required for Beanstalk operator is not installed")


class Plugin(abstract_json.AbstractPlugin):
    """Operator for Beanstalk work queue."""
    def __init__(self, host, port, queue_name, artifact_types=None,
            filter_string=None, allowed_sources=None, **kwargs):
        """Beanstalk operator."""
        self.queue = greenstalk.Client(host, port, use=queue_name)

        super(Plugin, self).__init__(artifact_types=artifact_types,
                                     filter_string=filter_string,
                                     allowed_sources=allowed_sources,
                                     **kwargs)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.URL,
        ]


    def _put(self, content):
        """Send content to a Beanstalk queue."""
        return self.queue.put(
            json.dumps(content)
        )
