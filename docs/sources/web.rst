.. _web-source:

Web
---

The **Web** source will periodically check a URL for changes, and extract any
artifacts it finds. This is useful for ingesting threat intel feeds that don't
already have a ThreatIngestor source plugin, without having to write your own
custom plugin. Use it for plaintext IP blacklists, C2 URL CSVs, and more.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``web``
* ``url`` (required): URL of the web content you want to poll.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: mylist
      module: web
      url: http://example.com/feed.txt
