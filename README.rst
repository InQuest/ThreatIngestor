.. raw:: html

    <p align="center">
      <img height="128" src="https://inquest.readthedocs.io/projects/threatingestor/en/latest/_static/threatingestor.png"  alt="threatingestor" title="threatingestor">
    </p>

    <h1 align="center">ThreatIngestor</h1>

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

An extendable tool to extract and aggregate IOCs from threat feeds.

Designed for use with `InQuest ThreatKB`_, but can be used without it.

Overview
--------

ThreatIngestor can be configured to watch Twitter, RSS feeds, or other
sources, extract meaningful information such as C2 IPs/domains and YARA
signatures, and send that information to another system for analysis.

Installation
------------

ThreatIngestor requires Python 3.6+.

Install ThreatIngestor and its dependencies::

    pip3 install -r requirements.txt
    python3 setup.py install

Usage
-----

Create a new ``config.yml`` file, and configure each source and operator module
you want to use. (See ``config.example.yml`` for layout.) Then run the script::

    threatingestor config.yml

By default, it will run forever, polling each configured source every 15
minutes.

For full documentation, see the `ThreatIngestor ReadTheDocs site`_.

Contributing
------------

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant.
By submitting a pull request you agree to release your submissions under the
terms of the LICENSE_.

.. _InQuest ThreatKB: https://github.com/InQuest/ThreatKB
.. _LICENSE: https://github.com/InQuest/threat-ingestors/blob/master/LICENSE
.. _ThreatIngestor ReadTheDocs site: https://threatingestor.readthedocs.io/
