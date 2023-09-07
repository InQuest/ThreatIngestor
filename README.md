<div align="center">
  <h1>ThreatIngestor</h1>
</div>

[![Build Status](https://github.com/InQuest/ThreatIngestor/actions/workflows/workflow.yml/badge.svg)](https://github.com/InQuest/ThreatIngestor/actions/workflows/workflow.yml)
![Documentation Status](https://readthedocs.org/projects/threatingestor/badge/?version=latest)
![PyPI Version](http://img.shields.io/pypi/v/ThreatIngestor.svg)

An extendable tool to extract and aggregate [IOCs](https://en.wikipedia.org/wiki/Indicator_of_compromise) from threat feeds.

Integrates out-of-the-box with [ThreatKB](https://github.com/InQuest/ThreatKB) and [MISP](https://www.misp-project.org/), and can fit seamlessly into any existing workflow with [SQS](https://aws.amazon.com/sqs/), [Beanstalk](https://beanstalkd.github.io/), and [custom plugins](https://inquest.readthedocs.io/projects/threatingestor/en/latest/developing.html).

Currently used by InQuest Labs IOC-DB: https://labs.inquest.net/iocdb

## Overview

ThreatIngestor can be configured to watch Twitter, RSS feeds, sitemap (XML) feeds, or other sources, and extract meaningful information such as malicious IPs/domains and YARA signatures, and send that information to another system for analysis.

![ThreatIngestor flowchart with several sources feeding into multiple operators](https://inquest.readthedocs.io/projects/threatingestor/en/latest/_images/mermaid-multiple-operators.png)

Try it out now with this [quick walkthrough](https://inquest.readthedocs.io/projects/threatingestor/en/latest/welcome.html#try-it-out), read more [ThreatIngestor walkthroughs](https://inquest.net/taxonomy/term/42) on the InQuest blog, and check out [labs.inquest.net/iocdb](https://labs.inquest.net/iocdb), an IOC aggregation and querying tool powered by ThreatIngestor.

## Installation

ThreatIngestor requires Python 3.6+, with development headers.

Install ThreatIngestor from PyPI:

```bash
pip install threatingestor
```

Install optional dependencies for using some plugins, as needed:

```bash
pip install threatingestor[all]
```

View the [full installation instructions](https://inquest.readthedocs.io/projects/threatingestor/en/latest/installation.html) for more information.

## Usage

Create a new ``config.yml`` file, and configure each source and operator module you want to use. (See ``config.example.yml`` for layout.) Then run the script:

```bash
threatingestor config.yml
```

By default, it will run forever, polling each configured source every 15 minutes.

If you'd like to run the image extraction source, or include the image extraction functionality for other sources, you will need to be running Python 3.7 >= due to the dependencies:

```bash
pip install opencv-python pytesseract numpy
```

View the [full ThreatIngestor documentation](https://inquest.readthedocs.io/projects/threatingestor/) for more information.

## Plugins

ThreatIngestor uses a plugin architecture with "source" (input) and "operator" (output) plugins. The currently supported integrations are:

### Sources

- [Git repositories](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/git.html)
- [GitHub repository search](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/github.html)
- [Gists by username](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/github_gist.html)
- [RSS feeds](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/rss.html)
- [Sitemap feeds](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/sitemap.html)
- [Image extraction](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/image.html)
- [Amazon SQS queues](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/sqs.html)
- [Twitter](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/twitter.html)
- [Generic web pages](https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/web.html)

### Operators

- [CSV files](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/csv.html)
- [MISP](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/misp.html)
- [MySQL table](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/mysql.html)
- [SQLite database](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/sqlite.html)
- [Amazon SQS queues](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/sqs.html)
- [ThreatKB](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/threatkb.html)
- [Twitter](https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/twitter.html)

View the [full ThreatIngestor documentation](https://inquest.readthedocs.io/projects/threatingestor/) for more information on included plugins, and how to create your own.

## Threat Intel Sources

Looking for some threat intel sources to get started? InQuest has a Twitter List with several accounts that post C2 domains and IPs: https://twitter.com/InQuest/lists/ioc-feed. Note that you will need to apply for a Twitter developer account to use the ThreatIngestor Twitter Source. Take a look at ``config.example.yml`` to see how to set this list up as a source.

For quicker setup, RSS feeds can be a great source of intelligence. Check out this example [RSS config file](https://github.com/InQuest/ThreatIngestor/blob/master/rss.example.yml) for a few pre-configured security blogs.

## Support

If you need help getting set up, or run into any issues, feel free to open an [issue](https://github.com/InQuest/ThreatIngestor/issues). You can also reach out to [@InQuest](https://twitter.com/InQuest) on Twitter or read more about us on the web at https://www.inquest.net.

We'd love to hear any feedback you have on ThreatIngestor, its documentation, or how you're putting it to work for you!

## Contributing

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant. By submitting a pull request you agree to release your submissions under the terms of the [LICENSE](https://github.com/InQuest/ThreatIngestor/blob/master/LICENSE).

## Docker


### Production

A `Dockerfile` is available for running ThreatIngestor within a Docker container.

First, you'll need to build the container:

```bash
docker build . -t threatingestor
```

After that, you can mount the container by using this command:

```bash
docker run -it --mount type=bind,source=/,target=/dock threatingestor /bin/bash
```

After you've mounted the container and you're inside the `/bin/bash` shell, you can run ThreatIngestor like normal:

```bash
threatingestor config.yml
```

### Development

There is also a Dockerfile.dev for building a development version of ThreatIngestor. All you need is an available .whl file, which can be generated with the following command:

```bash
python3 -m build 
```

After you've built the project, you can build the container:

```bash
docker build . -t threatingestor -f Dockerfile.dev
```

NOTE: If you run into any issues while building the development environment or running ThreatIngestor within the container, you may need to comment out the following lines in `Dockerfile.dev` to work properly:

```
FROM ubuntu:18.04
...
# RUN apt-get install tesseract-ocr -y
...
# RUN pip3 install opencv-python pytesseract numpy
...
```

### Extra Scripts

Some scripts are now provided to help with your local configuration of ThreatIngestor.

A README.md with additional information is available [here](https://github.com/InQuest/ThreatIngestor/tree/master/scripts/README.md).
