.. _source-plugins:

Source Plugins
==============

All source plugins maintain state between runs, allowing them to 

.. _twitter-source:

Twitter
-------

The **Twitter** source can use three Twitter API endpoints out of the box:
standard search, user timeline, and Twitter lists.

.. _rss-source:

RSS
---

The **RSS** source pulls from standard RSS and Atom feeds, and extracts
artifacts from within the feed content. It does not follow links to full
blog posts.

For each RSS feed, you'll need to define a ``feed_type`` for IOC extraction.
Valid feed types are:

* ``messy``: Only look at obfuscated URLs, assume all IPs are valid
* ``clean``: Treat everything as valid C2 URL/IP
* ``afterioc`` Treat everything after the last occurance of the string "Indicators
  of Compromise" as valid C2 URL/IP

.. _sqs-source:

SQS
---

The **SQS** source can be used to read content from `Amazon SQS` queues. This,
combined with the :ref:`SQS Operator <sqs-operator>`, allows a :ref:`full-circle
workflow <full-circle-workflow>`.

.. _web-source:

Web
---

The **Web** source will periodically check a URL for changes, and extract any
artifacts it finds. This is useful for ingesting threat intel feeds that don't
already have a ThreatIngestor source plugin, without having to write your own
custom plugin. Use it for plaintext IP blacklists, C2 URL CSVs, and more.

.. _git-source:

Git
---

The first time it's run, each **Git** source will clone the configured
repository, look for any files matching ``*.{rule,rules,yar,yara}``, and
extract YARA rules. On any subsequent runs, it will run ``git pull``, check for
new and updated files matching the same patterns, and extract YARA rules from
those files.

.. _github-source:

GitHub Repository Search
------------------------

The **GitHub** source plugin uses GitHub's `repository search API` to find new
interesting repos, and create a :ref:`Task artifact <task-artifact>` for each.
