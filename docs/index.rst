.. ThreatIngestor documentation master file, created by
   sphinx-quickstart on Thu Apr 19 10:17:12 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ThreatIngestor
==============

ThreatIngestor is a flexible, configuration-driven, extensible framework for
consuming threat intelligence.

It can watch Twitter, RSS feeds, and other sources, extract meaningful
information like C2 IPs/domains and YARA signatures, and send that information
to other systems for analysis.

Use ThreatIngestor alongside ThreatKB_ to automate importing public C2s and
YARA signatures, or integrate it into your existing workflow with :ref:`custom
operator plugins <custom-operator-plugins>`.

User Guide
----------

- Getting Started

 .. toctree::
    :maxdepth: 2

    installation
    basicusage

.. toctree::
   :maxdepth: 2

   artifacts

- Plugins

 .. toctree::
    :maxdepth: 2

    plugins/overview
    plugins/source
    plugins/operator

- Advanced Usage

 .. toctree::
    :maxdepth: 2

    workflows
    developing
    contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _ThreatKB: https://github.com/InQuest/ThreatKB
