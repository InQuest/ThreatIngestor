from threatingestor.operators import Operator
import threatingestor.artifacts

class AbstractPlugin(Operator):
    """Operator for Abstract JSON"""

    def __init__(self, artifact_types=None, filter_string=None, allowed_sources=None, **kwargs):
        # kwargs are used to dynamically form message body
        self.kwargs = kwargs

        super(AbstractPlugin, self).__init__(artifact_types=artifact_types,
                                     filter_string=filter_string,
                                     allowed_sources=allowed_sources)

        self.artifact_types = artifact_types or [
            threatingestor.artifacts.URL,
        ]

    def handle_artifact(self, artifact):
        """Operate on a single artifact"""
        message_body = dict([(k, artifact.format_message(v)) for (k, v) in self.kwargs.items()])
        self._put(message_body)

    def _put(self,content):
        raise NotImplementedError()
