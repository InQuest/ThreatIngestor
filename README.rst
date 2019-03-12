ThreatIngestor
==============

.. image:: https://inquest.net/images/inquest-badge.svg
    :target: https://inquest.net/
    :alt: Developed by InQuest
.. image:: https://travis-ci.org/InQuest/ThreatIngestor.svg?branch=master
    :target: https://travis-ci.org/InQuest/ThreatIngestor
    :alt: Build Status
.. image:: https://readthedocs.org/projects/threatingestor/badge/?version=latest
    :target: http://inquest.readthedocs.io/projects/threatingestor/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://api.codacy.com/project/badge/Grade/a989bb12e9604d5a9577ce71848e7a2a
    :target: https://app.codacy.com/app/InQuest/ThreatIngestor
    :alt: Code Health
.. image:: https://api.codacy.com/project/badge/Coverage/a989bb12e9604d5a9577ce71848e7a2a
    :target: https://app.codacy.com/app/InQuest/ThreatIngestor
    :alt: Test Coverage
.. image:: http://img.shields.io/pypi/v/ThreatIngestor.svg
    :target: https://pypi.python.org/pypi/ThreatIngestor
    :alt: PyPi Version

An extendable tool to extract and aggregate IOCs_ from threat feeds.

Integrates out-of-the-box with ThreatKB_ and MISP_, and can fit seamlessly into any existing worflow with SQS_, Beanstalk_, and `custom plugins`_.

Overview
--------

ThreatIngestor can be configured to watch Twitter, RSS feeds, or other sources, extract meaningful information such as malicious IPs/domains and YARA signatures, and send that information to another system for analysis.

`Try it out!`_

Installation
------------

ThreatIngestor requires Python 3.6+, with development headers.

Install ThreatIngestor from PyPI::

    pip install threatingestor

Install optional dependencies for using some plugins, as needed::

    pip install threatingestor[all]

View the `full installation instructions`_ for more information.

Usage
-----

Create a new ``config.yml`` file, and configure each source and operator module you want to use. (See ``config.example.yml`` for layout.) Then run the script::

    threatingestor config.yml

By default, it will run forever, polling each configured source every 15 minutes.

View the `full ThreatIngestor documentation`_ for more information.

Plugins
-------

ThreatIngestor uses a plugin architecture with "source" (input) and "operator" (output) plugins. The currently supported integrations are:

Sources
~~~~~~~

* Beanstalk work queues
* Git repositories
* GitHub repository search
* RSS feeds
* Amazon SQS queues
* Twitter
* Generic web pages

Operators
~~~~~~~~~

* Beanstalk work queues
* CSV files
* MISP
* SQLite database
* Amazon SQS queues
* ThreatKB
* Twitter

View the `full ThreatIngestor documentation`_ for more information on included plugins, and how to create your own.

Support
-------

If you need help getting set up, or run into any issues, feel free to open an Issue_. You can also reach out to `@InQuest`_ on Twitter.

We'd love to hear any feedback you have on ThreatIngestor, its documentation, or how you're putting it to work for you!

Contributing
------------

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant. By submitting a pull request you agree to release your submissions under the terms of the LICENSE_.

.. _ThreatKB: https://github.com/InQuest/ThreatKB
.. _LICENSE: https://github.com/InQuest/threat-ingestors/blob/master/LICENSE
.. _full ThreatIngestor Documentation: https://threatingestor.readthedocs.io/
.. _SQS: https://aws.amazon.com/sqs/
.. _Beanstalk: https://beanstalkd.github.io/
.. _MISP: https://www.misp-project.org/
.. _custom plugins: https://threatingestor.readthedocs.io/en/latest/developing.html
.. _IOCs: https://en.wikipedia.org/wiki/Indicator_of_compromise
.. _full installation instructions: https://threatingestor.readthedocs.io/en/latest/installation.html
.. _Issue: https://github.com/InQuest/ThreatIngestor/issues
.. _@InQuest: https://twitter.com/InQuest
.. _Try it out!: https://inquest.readthedocs.io/projects/threatingestor/en/latest/welcome.html#try-it-out
