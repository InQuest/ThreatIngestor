InQuest ThreatIngestor
======================

.. image:: https://inquest.net/images/inquest-badge.svg
    :target: https://inquest.net/
    :alt: Developed by InQuest

An extendable tool to extract and aggregate IOCs from threat feeds.

Designed for use with `InQuest ThreatKB`_, but can be used without it.

Overview
--------

ThreatIngestor can be configured to watch Twitter, RSS feeds, or other
sources, extract meaningful information such as C2 IPs/domains and YARA
signatures, and send that information to another system for analysis.

Installation
------------

Install ThreatIngestor and its dependencies::

    pip install -r requirements.txt
    python setup.py install

Usage
-----

Create a new ``config.ini`` file, and configure each source and operator module
you want to use. (See ``config.ini.example`` for layout.) Then run the script::

    python ingestor.py config.ini

Set ``daemon = true`` in the configuration file to have ThreatIngestor watch each
of your sources on a loop, or ``daemon = false`` if you'd rather run the script
on-demand or via a cron job you schedule yourself. The ``sleep`` value is ignored
if ``daemon`` is disabled.

For full documentation, see the `ThreatIngestor ReadTheDocs site`_.

Contributing
------------

Issues and pull requests are welcomed. Please keep Python code PEP8 compliant.
By submitting a pull request you agree to release your submissions under the
terms of the LICENSE_.

.. _InQuest ThreatKB: https://github.com/InQuest/ThreatKB
.. _LICENSE: https://github.com/InQuest/threat-ingestors/blob/master/LICENSE
.. _ThreatIngestor ReadTheDocs site: https://threatingestor.readthedocs.io/
