.. _rss-source:

RSS
---

The **RSS** source pulls from standard RSS and Atom feeds, and extracts
artifacts from within the feed content. It does not follow links to full
blog posts.

For each RSS feed, you'll need to define a ``feed_type`` for IOC extraction.
Valid feed types are:

* ``messy``: Only look at obfuscated URLs, assume all IPs are valid.
* ``clean``: Treat everything as valid C2 URL/IP.
* ``afterioc`` Treat everything after the last occurance of the string "Indicators
  of Compromise" as valid C2 URL/IP.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``rss``
* ``url`` (required): URL to the RSS or Atom feed.
* ``feed_type`` (required): see above; if unsure, use ``messy``.
* ``include`` (optional): Include filter using simplified regex.
* ``exclude`` (optional): Exclude filter using raw regex.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: rss-myiocfeed
      module: rss
      url: https://example.com/rss.xml
      feed_type: messy
      include: security|threat
      exclude: https:\/.inquest\.net\/blog[\/]?inquest-[\/]?

.. _sqs-source:

