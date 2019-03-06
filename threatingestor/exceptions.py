class IngestorError(Exception):
    """Base exception class."""
    pass

class DependencyError(IngestorError):
    """Missing dependency."""
    pass

class PluginError(IngestorError):
    """Missing plugin."""
    pass
