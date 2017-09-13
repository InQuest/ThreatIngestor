# InQuest ThreatIngestor

An extendable tool to extract and aggregate IOCs from threat feeds.

Designed for use with [InQuest ThreatKB](https://github.com/InQuest/ThreatKB).

## Overview

ThreatIngestor can be configured to watch Twitter lists, RSS feeds, or other
sources, extract meaningful information such as C2 IPs and domains, and send
that information to another system for analysis.

## Installation

Install ThreatIngestor and its dependencies:

```
pip install -r requirements.txt
python setup.py install
```

## Usage

Create a new `config.ini` file, and configure each source and operator module
you want to use. (See `config.ini.example` for layout.) Then run the script:

```
python ingestor.py config.ini
```

Set `daemon = true` in the configuration file to have ThreatIngestor watch each
of your sources on a loop, or `daemon = false` if you'd rather run the script
on-demand or via a cron job you schedule yourself. The `sleep` value is ignored
if `daemon` is disabled.

For each RSS feed, you'll need to define a `feed_type` for IOC extraction.
Valid feed types are:

* `messy`: Only look at obfuscated URLs, assume all IPs are valid
* `clean`: Treat everything as valid C2 URL/IP
* `afterioc` Treat everything after the last occurance of the string "Indicators
  of Compromise" as valid C2 URL/IP

## Plugins

ThreatIngestor can be easily extended to support other input and output
mechanisms through *Source* (input) and *Operator* (output) Python plugins. It
currently includes the following sources:

* Twitter
* RSS

And the following operators:

* ThreatKB
* CSV file

### Source Plugins

To add support for a new source, simply create a new Python file in the
`sources` folder (e.g. `examplesource.py`) and extend the `sources.Source`
class, overwriting both the `__init__` and `run` methods.

```python
from sources import Source

class ExampleSource(Source):

    def __init__(self, my_required_arg):
        """Args should be url, auth, etc, whatever is needed to set up the object."""
        self.my_required_arg = my_required_arg

    def run(self, saved_state):
        """Run and return (saved_state, list(Artifact))"""
        artifacts = []

        return saved_state, artifacts
```


You will most likely want to use the `sources.Source.process_element` method to
build the `artifacts` list. Check inline documentation, and see
`sources/twitter.py` and `sources/rss.py` for examples.

Once your module is complete, include it in `config.py` and it's ready to use.

```python
# in config.py
import sources.examplesource

SOURCE_MAP = {
    ...,
    'examplesource': sources.examplesource.ExampleSource,
}
```

Any arguments specified in `__init__` can be passed in from correspondingly
named keys in the `config.ini` section at runtime:

```
[source:myexample]
module = examplesource
my_required_arg = Some value
saved_state =
```

### Operator Plugins

Once artifacts are collected by a source plugin, they're sent to any
configured operator plugins for processing or export. Adding an operator
plugin is much the same as adding a source. Create a Python file in the
`operators` folder and extend the `operators.Operator` class, overwriting
the `__init__` and `handle_artifact` methods.

```python
import artifacts
from operators import Operator

class ExampleOperator(Operator):

    def __init__(self, my_required_arg):
        """Args should be url, auth, etc, whatever is needed to set up the object.

        Set self.artifact_types to a list of Artifacts supported by the plugin.
        """
        self.artifact_types = [artifacts.IPAddress, artifacts.Domain]

    def handle_artifact(self, artifact):
        """Override with the same signature"""
        # process artifact
```

Operators will only be run on artifacts in their `artifact_types` list.

Once your module is complete, include it in `config.py` and it's ready to use.

```python
# in config.py
import operators.exampleoperator

OPERATOR_MAP = {
    ...,
    'exampleoperator': operators.exampleoperator.ExampleOperator,
}
```

As with source modules, any arguments specified in `__init__` can be passed in
from correspondingly named keys in the `config.ini` section at runtime:

```
[operator:myexample]
module = exampleoperator
my_required_arg = Some value
```

## Contributing

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant.
By submitting a pull request you agree to release your submissions under the
terms of the [LICENSE](LICENSE).
