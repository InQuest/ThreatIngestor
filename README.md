# InQuest ThreatIngestor

An extendable tool to extract and aggregate IOCs from threat feeds.

Designed for use with [InQuest ThreatKB](https://github.com/InQuest/ThreatKB),
but can be used without it.

## Overview

ThreatIngestor can be configured to watch Twitter, RSS feeds, or other
sources, extract meaningful information such as C2 IPs and domains and YARA
signatures, and send that information to another system for analysis.

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
* SQS
* Web
* Git

And the following operators:

* ThreatKB
* CSV file
* Amazon SQS

The Twitter source can use three Twitter API endpoints out of the box: standard
search, user timeline, and Twitter lists. For examples of each, see
`config.ini.example`.

### Source Plugins

To add support for a new source, simply create a new Python file in the
`sources` folder (e.g. `examplesource.py`) and extend the `sources.Source`
class, overwriting both the `__init__` and `run` methods.

```python
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

    def __init__(self, my_required_arg, artifact_types=None, filter_string=None, allowed_sources=None):
        """Args should be url, auth, etc, whatever is needed to set up the object.

        Set self.artifact_types to a list of Artifacts supported by the plugin.
        """
        super(ExampleOperator, self).__init__(artifact_types, filter_string, allowed_sources)
        self.artifact_types = artifact_types or [artifacts.IPAddress, artifacts.Domain]

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

### Artifacts

Each configured source will be scraped and run through a series of pre- and
post-processors and regex searches to extract specific artifacts. The following
artifacts are currently supported:

* Domain
* IPAddress
* URL
* YARASignature
* Hash
* Task

Depending on the source type and feed type (see Usage section above), the
content of the sources will be parsed differently. For example, for both
Twitter and "messy" RSS feeds, we run the same processors to extract only
"obfuscated" URLs and domains, based on commonly occuring obfuscation patterns.
Any "word" with a dot surrounded with square brackets `[.]` we will attempt to
parse as a URL. Anything with a protocol specifier `://` will be picked up as a
URL automatically by the regex. All URLs are also stripped down and their
domains are included in the domain list. To ensure we only pick up obfuscated
URLs, we run a series of postprocessors (e.g. replace `[.]` with `.`, replace
`hxxp` with `http`, etc) and compare the result to the original; any that
differ are considered obfuscated and included in the output list. For "clean"
RSS feeds, we include all URLs, even if they aren't obfuscated in the source.
This allows us to ignore e.g. `http://t.co/` links in Tweets, and legitimate
non-C2 links in blog posts, while still picking up a majority of C2 mentions,
however inconsistent their obfuscation methods may be.

Below are some examples of URLs / domains that would be picked up by our
filters:

```
badguys[.]com
hxxp://badguys.com/bad/url
tcp://badguys[.]com:8989/bad
http://badguys(.)com
http://badguys[dot]com
http://badguys,com
http://badguys・com
http://badguys[.com
http://<strong>bad</strong>guys.com
```

Similar rules are followed for IP addresses. Note that loopback and private
addresses are automatically excluded from the output list, to help narrow down
the output to valid C2 hits.

## Contributing

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant.
By submitting a pull request you agree to release your submissions under the
terms of the [LICENSE](LICENSE).
