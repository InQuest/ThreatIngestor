.. _developing:

Developing
==========

Overview
--------

ThreatIngestor can be easily extended to support other input and output
mechanisms through *Source* (input) and *Operator* (output) Python plugins.

.. _custom-source-plugins:

Source Plugins
--------------

To add support for a new source, simply create a new Python file in the
``sources`` folder (e.g. ``examplesource.py``) and extend the ``sources.Source``
class, overwriting both the ``__init__`` and ``run`` methods::

    from sources import Source

    class ExampleSource(Source):

        def __init__(self, name, my_required_arg):
            """Args should be url, auth, etc, whatever is needed to set up the object.

            The name argument is required for all Source plugins, and is used internally.
            """
            self.name = name
            self.my_required_arg = my_required_arg

        def run(self, saved_state):
            """Run and return (saved_state, list(Artifact))"""
            artifacts = []

            return saved_state, artifacts


You will most likely want to use the ``sources.Source.process_element`` method to
build the ``artifacts`` list. Check inline documentation, and see
``sources/twitter.py`` and ``sources/rss.py`` for examples.

Once your module is complete, include it in ``config.py`` and it's ready to use::

    # in config.py
    import sources.examplesource

    SOURCE_MAP = {
        ...,
        'examplesource': sources.examplesource.ExampleSource,
    }

Any arguments specified in ``__init__`` can be passed in from correspondingly
named keys in the ``config.ini`` section at runtime::

    [source:myexample]
    module = examplesource
    my_required_arg = Some value
    saved_state =

.. _custom-operator-plugins:

Operator Plugins
----------------

Once artifacts are collected by a source plugin, they're sent to any
configured operator plugins for processing or export. Adding an operator
plugin is much the same as adding a source. Create a Python file in the
``operators`` folder and extend the ``operators.Operator`` class, overwriting
the ``__init__`` and ``handle_artifact`` methods::

    import artifacts
    from operators import Operator

    class ExampleOperator(Operator):

        def __init__(self, my_required_arg, artifact_types=None, filter_string=None, allowed_sources=None):
            """Args should be url, auth, etc, whatever is needed to set up the object.

            Set self.artifact_types to a list of Artifacts supported by the plugin.
            """
            super(ExampleOperator, self).__init__(artifact_types, filter_string, allowed_sources)
            self.artifact_types = artifact_types or [artifacts.IPAddress, artifacts.Domain]

        def handle_artifact(self, artifact):
            """Override with the same signature"""
            # process artifact

Operators will only be run on artifacts in their ``artifact_types`` list.

Once your module is complete, include it in ``config.py`` and it's ready to use::

    # in config.py
    import operators.exampleoperator

    OPERATOR_MAP = {
        ...,
        'exampleoperator': operators.exampleoperator.ExampleOperator,
    }

As with source modules, any arguments specified in ``__init__`` can be passed in
from correspondingly named keys in the ``config.ini`` section at runtime::

    [operator:myexample]
    module = exampleoperator
    my_required_arg = Some value
