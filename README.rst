ThreatIngestor
==============

.. image:: https://inquest.net/images/inquest-badge.svg
    :target: https://inquest.net/
    :alt: Developed by InQuest
.. image:: https://travis-ci.org/InQuest/ThreatIngestor.svg?branch=master
    :target: https://travis-ci.org/InQuest/ThreatIngestor
    :alt: Build Status (Travis CI)

.. Change ?branch=develop to ?branch=master when merging into master
.. image:: https://github.com/InQuest/ThreatIngestor/workflows/threatingestor-workflow/badge.svg?branch=develop
    :target: https://github.com/InQuest/ThreatIngestor/actions
    :alt: Build Status (GitHub Workflow)

.. image:: https://readthedocs.org/projects/threatingestor/badge/?version=latest
    :target: http://inquest.readthedocs.io/projects/threatingestor/en/latest/?badge=latest
    :alt: Documentation Status
.. .. image:: https://api.codacy.com/project/badge/Grade/a989bb12e9604d5a9577ce71848e7a2a
..     :target: https://app.codacy.com/app/InQuest/ThreatIngestor
..     :alt: Code Health
.. .. image:: https://api.codacy.com/project/badge/Coverage/a989bb12e9604d5a9577ce71848e7a2a
..     :target: https://app.codacy.com/app/InQuest/ThreatIngestor
..     :alt: Test Coverage
.. image:: http://img.shields.io/pypi/v/ThreatIngestor.svg
    :target: https://pypi.python.org/pypi/ThreatIngestor
    :alt: PyPi Version

An extendable tool to extract and aggregate IOCs_ from threat feeds.

Integrates out-of-the-box with ThreatKB_ and MISP_, and can fit seamlessly into any existing workflow with SQS_, Beanstalk_, and `custom plugins`_.

Currently used by InQuest Labs IOC-DB: https://labs.inquest.net/iocdb.

Overview
--------

ThreatIngestor can be configured to watch Twitter, RSS feeds, or other sources, extract meaningful information such as malicious IPs/domains and YARA signatures, and send that information to another system for analysis.

.. image:: https://inquest.readthedocs.io/projects/threatingestor/en/latest/_images/mermaid-multiple-operators.png
    :target: https://inquest.readthedocs.io/projects/threatingestor/en/latest/workflows.html
    :alt: ThreatIngestor flowchart with several sources feeding into multiple operators.

Try it out now with this `quick walkthrough`_, read more `ThreatIngestor walkthroughs`_ on the InQuest blog, and check out `labs.inquest.net/iocdb`_, an IOC aggregation and querying tool powered by ThreatIngestor.

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

* `Beanstalk work queues <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/beanstalk.html>`__
* `Git repositories <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/git.html>`__
* `GitHub repository search <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/github.html>`__
* `Gists by username <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/github_gist.html>`__
* `RSS feeds <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/rss.html>`__
* `Sitemap blogs <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/sitemap.html>`__
* `Image extraction <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/image.html>`__
* `Amazon SQS queues <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/sqs.html>`__
* `Twitter <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/twitter.html>`__
* `Generic web pages <https://inquest.readthedocs.io/projects/threatingestor/en/latest/sources/web.html>`__

Operators
~~~~~~~~~

* `Beanstalk work queues <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/beanstalk.html>`__
* `CSV files <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/csv.html>`__
* `MISP <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/misp.html>`__
* `MySQL table <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/mysql.html>`__
* `SQLite database <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/sqlite.html>`__
* `Amazon SQS queues <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/sqs.html>`__
* `ThreatKB <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/threatkb.html>`__
* `Twitter <https://inquest.readthedocs.io/projects/threatingestor/en/latest/operators/twitter.html>`__

View the `full ThreatIngestor documentation`_ for more information on included plugins, and how to create your own.

Threat Intel Sources
--------------------

Looking for some threat intel sources to get started? InQuest has a Twitter List with several accounts that post C2 domains and IPs: https://twitter.com/InQuest/lists/ioc-feed. Note that you will need to apply for a Twitter developer account to use the ThreatIngestor Twitter Source. Take a look at ``config.example.yml`` to see how to set this list up as a source.

For quicker setup, RSS feeds can be a great source of intelligence. Check out this example `RSS config file`_ for a few pre-configured security blogs.

Support
-------

If you need help getting set up, or run into any issues, feel free to open an Issue_. You can also reach out to `@InQuest`_ on Twitter or read more about us on the web at https://www.inquest.net.

We'd love to hear any feedback you have on ThreatIngestor, its documentation, or how you're putting it to work for you!

Contributing
------------

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant. By submitting a pull request you agree to release your submissions under the terms of the LICENSE_.

.. _ThreatKB: https://github.com/InQuest/ThreatKB
.. _LICENSE: https://github.com/InQuest/threat-ingestors/blob/master/LICENSE
.. _full ThreatIngestor Documentation: https://inquest.readthedocs.io/projects/threatingestor/
.. _SQS: https://aws.amazon.com/sqs/
.. _Beanstalk: https://beanstalkd.github.io/
.. _MISP: https://www.misp-project.org/
.. _custom plugins: https://inquest.readthedocs.io/projects/threatingestor/en/latest/developing.html
.. _IOCs: https://en.wikipedia.org/wiki/Indicator_of_compromise
.. _full installation instructions: https://inquest.readthedocs.io/projects/threatingestor/en/latest/installation.html
.. _Issue: https://github.com/InQuest/ThreatIngestor/issues
.. _@InQuest: https://twitter.com/InQuest
.. _quick walkthrough: https://inquest.readthedocs.io/projects/threatingestor/en/latest/welcome.html#try-it-out
.. _ThreatIngestor walkthroughs: https://inquest.net/taxonomy/term/42
.. _RSS config file: https://github.com/InQuest/ThreatIngestor/blob/master/rss.example.yml
.. _labs.inquest.net/iocdb: https://labs.inquest.net/iocdb

Docker Container
----------------

A Dockerfile is now available for running ThreatIngestor within a Docker container.

First, you'll need to build the container::

    docker build . -t threat

After that, you can mount the container for use using this command::

    docker run -it --mount type=bind,source=/,target=/dock threat /bin/bash

After you've mounted the container, and you're inside of the `/bin/bash` shell, you can run the threatingestor like normal::
    
    threatingestor config.yml