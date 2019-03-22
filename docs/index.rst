.. ThreatIngestor documentation master file, created by
   sphinx-quickstart on Thu Apr 19 10:17:12 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. raw:: html

    <p align="center">
      <img height="128" src="https://inquest.readthedocs.io/projects/threatingestor/en/latest/_static/threatingestor.png"  alt="threatingestor" title="threatingestor">
    </p>

    <h1 align="center">ThreatIngestor</h1>

ThreatIngestor is a flexible, configuration-driven, extensible framework for consuming threat intelligence.

It can watch Twitter, RSS feeds, and other sources, extract meaningful information like :term:`C2` IPs/domains and YARA signatures, and send that information to other systems for analysis.

Use ThreatIngestor alongside ThreatKB_ or MISP_ to automate importing public C2s and YARA signatures, or integrate it into your existing workflow with :ref:`custom operator plugins <custom-operator-plugins>`.

User Guide
----------


.. toctree::
   :maxdepth: 2

   welcome
   installation
   basicusage
   workflows

.. toctree::
   :maxdepth: 1

   sources
   operators

.. toctree::
   :maxdepth: 2

   artifacts
   extras

.. toctree::
   :maxdepth: 1

   observability
   developing
   api

.. toctree::
   :hidden:

   glossary

* :ref:`genindex`
* :ref:`modindex`
* :ref:`glossary`

.. _ThreatKB: https://github.com/InQuest/ThreatKB
.. _MISP: https://www.misp-project.org/
