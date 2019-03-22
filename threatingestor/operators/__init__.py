import re


from loguru import logger


class Operator:
    """Base class for all Operator plugins.

    Note: This is an abstract class. You must extend ``__init__`` and call
    ``super`` to ensure this class's constructor is called. You must override
    ``handle_artifact`` with the same signature. You may define additional
    ``handle_{artifact_type}`` methods as needed (see the threatkb operator for
    an example) - these methods are purely convention, and are not required.

    When adding additional methods to child classes, consider prefixing the
    method name with an underscore to denote a ``_private_method``. Do not
    override other existing methods from this class.
    """
    def __init__(self, artifact_types=None, filter_string=None, allowed_sources=None):
        """Override this constructor in child classes.

        The arguments above (artifact_types, filter_string, allowed_sources)
        should be accepted explicity as above, in all child classes.

        Additional arguments should be added: url, auth, etc, whatever is
        needed to set up the object.

        Each operator should default self.artifact_types to a list of Artifacts
        supported by the plugin, and allow passing in artifact_types to
        overwrite that default.

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
        """Override with the same signature.

        :param artifact: A single ``Artifact`` object.
        :returns: None (always ignored)
        """
        raise NotImplementedError()


    def _artifact_is_allowed(self, artifact):
        """Returns True iff this artifact is allowed by this plugin's filters."""
        # Must be in allowed_types.
        if not any(isinstance(artifact, t) for t in self.artifact_types):
            return False

        # Must match the filter string.
        if not artifact.match(self.filter_string):
            return False

        # Must be in allowed_sources, if set.
        if self.allowed_sources and not any(
                [re.compile(p).search(artifact.source_name)
                 for p in self.allowed_sources]):
            return False

        return True


    def process(self, artifacts):
        """Process all applicable artifacts."""
        for artifact in artifacts:
            if self._artifact_is_allowed(artifact):
                self.handle_artifact(artifact)
