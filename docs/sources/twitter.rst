.. _twitter-source:

Twitter
-------

The **Twitter** source can use several Twitter API endpoints out of the box:
@mentions, Twitter lists, user timeline, and standard search.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``twitter``
* ``api_key`` (required): Consumer API key (See `Twitter oauth docs`_).
* ``api_secret_key`` (required): Consumer API secret key (See `Twitter oauth docs`_).
* ``access_token`` (required): Twitter access token (See `Twitter oauth docs`_).
* ``access_token_secret`` (required): Twitter access token secret (See `Twitter oauth docs`_).
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
        api_key: MY_KEY
        api_secret_key: MY_SECRET_KEY
        access_token: MY_TOKEN
        access_token_secret: MY_TOKEN_SECRET

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

.. _Twitter oauth docs: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
.. _Twitter list: https://dev.twitter.com/rest/reference/get/lists/statuses
.. _Twitter user timeline: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
.. _Twitter search: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
.. _Mentions: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-mentions_timeline.html
