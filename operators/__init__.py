class Operator:
    """Base class, see method documentation"""

    def __init__(self, artifact_types=None, filter_string=None):
        """Args should be url, auth, etc, whatever is needed to set up the object.

        The artifact_types arg should be accepted either explicity as above, or
        via kwargs.

        Each operator should default self.artifact_types to a list of Artifacts
        supported by the plugin, and allow passing in artifact_types to overwrite
        that default.

        Example:

        >>> self.artifact_types = artifact_types or [
        ...     artifacts.IPAddress,
        ...     artifacts.Domain,
        ... ]
        """
        self.artifact_types = artifact_types or []
        self.filter_string = filter_string or ''

    def handle_artifact(self, artifact):
        """Override with the same signature"""
        raise NotImplementedError()

    def process(self, artifacts):
        """Process all applicable artifacts"""
        for artifact in artifacts:
            if any(isinstance(artifact, t) for t in self.artifact_types) and artifact.match(self.filter_string):
                self.handle_artifact(artifact)
