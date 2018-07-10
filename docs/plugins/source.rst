.. _source-plugins:

Source Plugins
==============

Source plugins handle artifact import. All source plugins maintain state
between runs, allowing them to skip previously processed tweets, blog posts,
etc and get right to work finding new indicators.

To add an source to your configuration file, include a section like this:

.. code-block:: ini

    [source:mysource]
    module = mysourcemodule
    saved_state =

ThreatIngestor looks for sections matching ``source:``, and uses the rest
of the section name as the source name. The ``module`` option must match
one of the sources listed below, or your :ref:`custom source
<custom-source-plugins>`. Leave the ``saved_state`` value blank, and it will
be filled in automatically when the source runs.

.. _twitter-source:

Twitter
-------

The **Twitter** source can use three Twitter API endpoints out of the box:
Twitter lists, user timeline, and standard search.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``twitter``
* ``saved_state`` (required): leave blank; will be filled with a tweet ID.
* ``token`` (required): Twitter auth token (See `Twitter oauth docs`_).
* ``token_key`` (required): Twitter auth token key (See `Twitter oauth docs`_).
* ``con_secret_key`` (required): Twitter auth connection secret key (See
  `Twitter oauth docs`_).
* ``con_secret`` (required): Twitter auth connection secret (See `Twitter oauth
  docs`_).

After the above required options, you must include valid options for one of the
three supported Twitter endpoints, as described below. Any extra options
defined in the config will be passed in directly to the Twitter endpoint, so
you can configure some extra options not shown here. See the relevant Twitter
documentation for more information on supported parameters.

`Twitter list`_:

* ``owner_screen_name``: Twitter user who owns the list.
* ``slug``: The name of the Twitter list.

`Twitter user timeline`_:

* ``screen_name``: Twitter user to watch.

`Twitter search`_:

* ``q``: Twitter search term, can be multiple words including hashtags.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Twitter list:

.. code-block:: ini

    [source:twitter-inquest-c2-list]
    module = twitter
    saved_state =
    token = MYTOKEN
    token_key = MYTOKENKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    owner_screen_name = InQuest
    slug = c2-feed

Twitter user timeline:

.. code-block:: ini

    [source:twitter-inquest-timeline]
    module = twitter
    saved_state =
    token = MYTOKEN
    token_key = MYTOKENKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    screen_name = InQuest

Twitter search:

.. code-block:: ini

    [source:twitter-open-directory]
    module = twitter
    saved_state =
    token = MYTOKEN
    token_key = MYTOKENKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    q = "open directory" #malware

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
* ``saved_state`` (required): leave blank; will be filled with a parsable datetime.
* ``feed_type`` (required): see above; if unsure, use ``messy``.
* ``url`` (required): URL to the RSS or Atom feed.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [source:rss-myiocfeed]
    module = rss
    saved_state =
    url = https://example.com/rss.xml
    feed_type = messy

.. _sqs-source:

SQS
---

The **SQS** source can be used to read content from `Amazon SQS`_ queues. This,
combined with the :ref:`SQS Operator <sqs-operator>`, allows a :ref:`full-circle
workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sqs``
* ``saved_state`` (required): leave blank; not used (SQS jobs are deleted
  once processed).
* ``aws_access_key_id`` (required): Your AWS access key ID.
* ``aws_secret_access_key`` (required): Your AWS secret access key.
* ``aws_region`` (required): Your AWS region name.
* ``queue_name`` (required): The name of the SQS queue you want to use.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [source:sqs-input]
    module = sqs
    saved_state =
    aws_access_key_id = MYKEY
    aws_secret_access_key = MYSECRET
    aws_region = MYREGION
    queue_name = MYQUEUENAME

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
* ``saved_state`` (required): leave blank; will be filled with HTTP
  ``Last-Modified`` / ``ETag`` header contents, as appropriate.
* ``url`` (required): URL of the web content you want to poll.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [source:mylist]
    module = web
    saved_state =
    url = http://example.com/feed.txt

.. _git-source:

Git
---

The first time it's run, each **Git** source will clone the configured
repository, look for any files matching ``*.{rule,rules,yar,yara}``, and
extract YARA rules. On any subsequent runs, it will run ``git pull``, check for
new and updated files matching the same patterns, and extract YARA rules from
those files.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``git``
* ``saved_state`` (required): leave blank; will be filled with a commit hash.
* ``url`` (required): URL (can be https, git, ssh, etc) of remote to clone.
* ``local_path`` (required): folder on disk (relative or absolute) to clone into.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [source:inquest-yara-rules]
    module = git
    saved_state =
    url = https://github.com/InQuest/yara-rules.git
    local_path = /opt/threatingestor/git/yara-rules

.. _github-source:

GitHub Repository Search
------------------------

The **GitHub** source plugin uses GitHub's `repository search API`_ to find new
interesting repos, and create a :ref:`Task artifact <task-artifact>` for each.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``github``
* ``saved_state`` (required): leave blank; will be filled with a timestamp.
* ``search`` (required): search term(s).

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

.. _Twitter oauth docs: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
.. _Twitter list: https://dev.twitter.com/rest/reference/get/lists/statuses
.. _Twitter user timeline: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
.. _Twitter search: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
.. _Amazon SQS: https://aws.amazon.com/sqs/
.. _repository search API: https://developer.github.com/v3/search/#search-repositories
