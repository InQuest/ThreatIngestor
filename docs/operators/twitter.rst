.. _twitter-operator:

Twitter
-------

The Twitter operator will send custom messages including details of extracted
artifacts as Tweets. It supports quote-tweeting the original source of the
artifact, if that source was also a Tweet.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``twitter``
* ``token`` (required): Twitter auth token (See `Twitter oauth docs`_).
* ``token_key`` (required): Twitter auth token key (See `Twitter oauth docs`_).
* ``con_secret_key`` (required): Twitter auth connection secret key (See
  `Twitter oauth docs`_).
* ``con_secret`` (required): Twitter auth connection secret (See `Twitter oauth
  docs`_).
* ``status`` (required): The text to send with each Tweet. (Interpolated by
  ``Artifact.format_message``.)

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following example assumes Twitter credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: twitter-auth
        token: MYTOKEN
        token_key: MYTOKENKEY
        con_secret_key: MYSECRETKEY
        con_secret: MYSECRET

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: mytwitterbot
      module: twitter
      credentials: twitter-auth
      status: '{reference_text} #iocs'

.. note::

    When including hashtags in the status, be sure to put quotes around your
    status text, as shown in the example above. Otherwise, the ``#``
    character will be treated as the beginning of a YAML comment.

.. _Twitter oauth docs: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
