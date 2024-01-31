from ddtrace import tracer
from ddtrace.profiling import Profiler

from threatingestor.operators import Operator

class Plugin(Operator):
    """
    Operator for activating DataDog APM
    """

    def __init__(self, hostname=None, port=None, https=False, artifact_types=None, filter_string=None, allowed_sources=None):
        """
        DataDog operator
        """

        self.tracer = tracer.configure(hostname=hostname, port=port, https=https)
        self.profile = Profiler()
