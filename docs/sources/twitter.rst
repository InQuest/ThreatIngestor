.. _twitter-source:

Twitter / X
-----------

The **Twitter** (**X**) source can use several Twitter API endpoints out of the box:
Twitter lists, user timeline, and standard search.

.. note::
  
  Due to the recent Twitter v2.0 paid transition, ThreatIngestor only supports endpoints up to the **Basic** plan. As the Twitter API evolves, some issues may arise.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``twitter``
* ``api_key`` (required): Consumer API key (See `Twitter oauth docs`_).
* ``api_secret_key`` (required): Consumer API secret key (See `Twitter oauth docs`_).
* ``access_token`` (required): Twitter access token (See `Twitter oauth docs`_).
* ``access_token_secret`` (required): Twitter access token secret (See `Twitter oauth docs`_).
* ``bearer_token`` (required): Twitter bearer token (v2) (See `Twitter oauth docs`_).
* ``defanged_only``: Defaults to ``true``. If set to ``false``, the Twitter
  source will include all expanded links found in Tweets. If set to ``true``,
  it will include only defanged links.

After the above general options, you may include valid options for one of the supported Twitter endpoints, as described below. Any extra options defined in the config will be passed in directly to the Twitter endpoint, so you can configure some extra options not shown here. See the relevant Twitter documentation for more information on supported parameters.

`Twitter list`_:

* ``list_id``: Id of the list you want to ingest.

`Twitter user timeline`_:

* ``username``: Username of Twitter user to watch.
* ``user_id``: User ID of Twitter user to watch.

`Twitter search`_:

* ``query``: Twitter search term, can be multiple words including hashtags.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following examples all assume Twitter credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: twitter-auth
        api_key: MY_KEY
        api_secret_key: MY_SECRET_KEY
        access_token: MY_TOKEN
        access_token_secret: MY_TOKEN_SECRET
        bearer_token: MY_BEARER_TOKEN

Inside the ``sources`` section of the config, create a new item for the source
you wish to define. Examples for each of the supported Twitter endpoints are
provided below.

Twitter list:

.. code-block:: yaml

    - name: twitter-inquest-ioc-feed
      module: twitter
      credentials: twitter-auth
      list_id: 917864294053752832

Twitter user timeline:

.. code-block:: yaml

    - name: twitter-inquest-timeline
      module: twitter
      credentials: twitter-auth
      username: InQuest

Twitter search:

.. code-block:: yaml

    - name: twitter-opendir
      module: twitter
      credentials: twitter-auth
      query: '"open directory" #malware'

.. note::

    When searching for Twitter hashtags, be sure to put quotes around your
    search term, as shown in the example above. Otherwise, the ``#``
    character will be treated as the beginning of a YAML comment.

.. _Twitter oauth docs: https://developer.twitter.com/en/docs/authentication/oauth-2-0
.. _Twitter list: https://developer.twitter.com/en/docs/twitter-api/lists/list-tweets/api-reference/get-lists-id-tweets
.. _Twitter user timeline: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
.. _Twitter search: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
