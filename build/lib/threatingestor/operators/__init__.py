import re

class Operator(object):
    """Base class, see method documentation"""

    def __init__(self, artifact_types=None, filter_string=None, allowed_sources=None):
        """Args should be url, auth, etc, whatever is needed to set up the object.

        The arguments above (artifact_types, filter_string, allowed_sources) should
        be accepted either explicity as above, or via kwargs.

        Each operator should default self.artifact_types to a list of Artifacts
        supported by the plugin, and allow passing in artifact_types to overwrite
        that default.

        Example:

        >>> self.artifact_types = artifact_types or [
        ...     artifacts.IPAddress,
        ...     artifacts.Domain,
        ... ]

        It's recommended to call this __init__ method via super from all child
        classes. Remember to do so *before* setting any default artifact_types.
        """
        self.artifact_types = artifact_types or []
        self.filter_string = filter_string or ''
        self.allowed_sources = allowed_sources or []

    def handle_artifact(self, artifact):
        """Override with the same signature"""
        raise NotImplementedError()

    def _artifact_is_allowed(self, artifact):
        # must be in allowed_types
        if not any(isinstance(artifact, t) for t in self.artifact_types):
            return False

        # must match the filter string
        if not artifact.match(self.filter_string):
            return False

        # must be in allowed_sources, if set
        if self.allowed_sources and not any([re.compile(p).search(artifact.source_name) for p in self.allowed_sources]):
            return False

        return True

    def process(self, artifacts):
        """Process all applicable artifacts"""
        for artifact in artifacts:
            if self._artifact_is_allowed(artifact):
                self.handle_artifact(artifact)
