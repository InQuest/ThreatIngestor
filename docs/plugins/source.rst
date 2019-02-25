.. _source-plugins:

Source Plugins
==============

For each source specified, ``ThreatIngestor`` handles artifact import. Sources
may link to Twitter, Blogs, etc. Artifacts are imported from those sources and
could include URLs, IP Addresses, YARA Signatures, etc. All source plugins
maintain state between runs, allowing them to skip previously processed
artifacts and get right to work finding new indicators.

To add a source to your configuration file, include a section like this:

.. code-block:: yaml

    sources:
      - name: mysource
        module:  mysourcemodule

You can add as many sources as you need, all under the same ``sources:`` list.

.. code-block:: yaml

    sources:
      - name: mysource
        module: mysourcemodule

      - name: myothersource
        module: mysourcemodule

Note the use of dashes to signify the start of each item in the list, and
matching indentation for all the keys within each item.

The ``module`` option must match one of the sources listed below, or your
:ref:`custom source <custom-source-plugins>`. The ``name`` is freeform.

All sources allow credentials such as usernames, passwords, OAuth tokens, etc
to be defined in a seperate ``credentials`` section and referenced by name with
a ``credentials`` keyword. Consider a plugin that accepts a ``token`` and a
``secret``. In ``config.yml``, you would set it up the ``credentials`` and
``sources`` sections like this:

.. code-block:: yaml

    credentials:
      - name: mysource-auth
        token: MYTOKEN
        secret: MYSECRET

    sources:
      - name: mysource
        credentials: mysource-auth

This allows the same credentials to be reused for several different sources
(or operators) without having to duplicate them in each source definition.

.. _twitter-source:

Twitter
-------

The **Twitter** source can use several Twitter API endpoints out of the box:
@mentions, Twitter lists, user timeline, and standard search.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``twitter``
* ``token`` (required): Twitter auth token (See `Twitter oauth docs`_).
* ``token_key`` (required): Twitter auth token key (See `Twitter oauth docs`_).
* ``con_secret_key`` (required): Twitter auth connection secret key (See
  `Twitter oauth docs`_).
* ``con_secret`` (required): Twitter auth connection secret (See `Twitter oauth
  docs`_).
* ``defanged_only``: Defaults to ``true``. If set to ``false``, the Twitter
  source will include all expanded links found in Tweets. If set to ``true``,
  it will include only defanged links.

After the above general options, you may include valid options for one of the
supported Twitter endpoints, as described below. (If you do not include any
extra options, the Twitter plugin will default to reading from your @mentions.)
Any extra options defined in the config will be passed in directly to the
Twitter endpoint, so you can configure some extra options not shown here. See
the relevant Twitter documentation for more information on supported parameters.

`Mentions`_:

This is the default behavior.

`Twitter list`_:

* ``owner_screen_name``: Twitter user who owns the list.
* ``slug``: The name of the Twitter list.

`Twitter user timeline`_:

* ``screen_name``: Twitter user to watch.

`Twitter search`_:

* ``q``: Twitter search term, can be multiple words including hashtags.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following examples all assume Twitter credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: twitter-auth
        token: MYTOKEN
        token_key: MYTOKENKEY
        con_secret_key: MYSECRETKEY
        con_secret: MYSECRET

Inside the ``sources`` section of the config, create a new item for the source
you wish to define. Examples for each of the supported Twitter endpoints are
provided below.

Mentions:

.. code-block:: yaml

    - name: twitter-my-mentions
      module: twitter
      credentials: twitter-auth

Twitter list:

.. code-block:: yaml

    - name: twitter-inquest-c2-list
      module: twitter
      credentials: twitter-auth
      owner_screen_name: InQuest
      slug: c2-feed

Twitter user timeline:

.. code-block:: yaml

    - name:twitter-inquest-timeline
      module: twitter
      credentials: twitter-auth
      screen_name: InQuest

Twitter search:

.. code-block:: yaml

    - name: twitter-open-directory
      module: twitter
      credentials: twitter-auth
      q: '"open directory" #malware'

.. note::

    When searching for Twitter hashtags, be sure to put quotes around your
    search term, as shown in the example above. Otherwise, the ``#``
    character will be treated as the beginning of a YAML comment.

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
* ``feed_type`` (required): see above; if unsure, use ``messy``.
* ``url`` (required): URL to the RSS or Atom feed.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: rss-myiocfeed
      module: rss
      url: https://example.com/rss.xml
      feed_type: messy

.. _sqs-source:

SQS
---

The **SQS** source can be used to read content from `Amazon SQS`_ queues. This,
combined with the :ref:`SQS Operator <sqs-operator>`, allows a :ref:`full-circle
workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sqs``
* ``aws_access_key_id`` (required): Your AWS access key ID.
* ``aws_secret_access_key`` (required): Your AWS secret access key.
* ``aws_region`` (required): Your AWS region name.
* ``queue_name`` (required): The name of the SQS queue you want to use.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following example assumes AWS credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: aws-auth
        aws_access_key_id: MYKEY
        aws_secret_access_key: MYSECRET
        aws_region: MYREGION

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: sqs-input
      module: sqs
      credentials: aws-auth
      queue_name: MYQUEUENAME

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
* ``url`` (required): URL (can be https, git, ssh, etc) of remote to clone.
* ``local_path`` (required): folder on disk (relative or absolute) to clone into.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: inquest-yara-rules
      module: git
      url: https://github.com/InQuest/yara-rules.git
      local_path: /opt/threatingestor/git/yara-rules

.. _github-source:

GitHub Repository Search
------------------------

The **GitHub** source plugin uses GitHub's `repository search API`_ to find new
interesting repos, and create a :ref:`Task artifact <task-artifact>` for each.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``github``
* ``search`` (required): search term(s).

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: github-cve-repos
      module: github
      search: CVE-2018-

Beanstalk
---------

The **Beanstalk** source can be used to read content from `Beanstalk`_ queues.
This, combined with the :ref:`Beanstalk Operator <beanstalk-operator>`, allows
a :ref:`full-circle workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``beanstalk``
* ``host`` (required): Host to connect to.
* ``port`` (required): Port to connect over.
* ``queue_name`` (required): The name of the Beanstalk queue you want to use.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: beanstalk-input
      module: beanstalk
      host: 127.0.0.1
      port: 11300
      queue_name: MYQUEUENAME

.. _Twitter oauth docs: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
.. _Twitter list: https://dev.twitter.com/rest/reference/get/lists/statuses
.. _Twitter user timeline: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
.. _Twitter search: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
.. _Mentions: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline.html
.. _Amazon SQS: https://aws.amazon.com/sqs/
.. _repository search API: https://developer.github.com/v3/search/#search-repositories
.. _Beanstalk: https://beanstalkd.github.io/
