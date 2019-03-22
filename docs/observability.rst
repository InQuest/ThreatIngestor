Observability
=============

ThreatIngestor comes with a few configurable options for observability_:

* Logging
* Metrics
* Notifications

By default, ThreatIngestor will print some debug logs to ``stderr``, and will send some basic metrics to a local ``statsd`` server on the default port, if it finds one.

Logging
-------

ThreatIngestor uses Loguru_ for logging, and will pass in any config you define in your ``config.yml`` in a ``logging:`` section.

Any options accepted by Loguru's configure_ function can be defined in your ``config.yml``. You can also use the supported `environment variables`_ to change logging options without modifying the config.

Metrics
-------

ThreatIngestor uses statsd_, through the python-statsd_ library, to track a few different types of metrics. If you'd like to track counts for each type of artifact, error rates, how long it takes your sources/operators to run, set up a statsd server and point it to a frontend like Graphite or a (paid) service like Datadog or Librato.

Any options accepted by StatsClient_ can be defined in your ``config.yml``, in a ``statsd`` section.

For example:

.. code-block:: yaml

    statsd:
        prefix: 'threatingestor'

This will tell ThreatIngestor to prefix all its metrics with ``threatingestor``, which is useful if you have more than one tool feeding into your statsd server.

Notifications
-------------

ThreatIngestor uses Notifiers_ for notifications, and will pass in any config you define in your ``config.yml`` in a ``notifiers:`` section.

Notifiers supports several providers, including email, common chat serices, push notifications, and more.

Here's an example using HipChat:

.. code-block:: yaml

    notifiers:
        provider: hipchat
        defaults:
            team_server: https://myteamserver
            room: 'ROOMID'
            token: MYTOKEN
            id: ID
            message_format: text
            notify: false

For documentation on required parameters for each provider, take a look at the `Notifiers Providers docs`_. Anything you define in the config will be passed into this NotificationHandler_ logging interface.

.. _observability: https://en.wikipedia.org/wiki/Observability
.. _Loguru: https://loguru.readthedocs.io/en/stable/
.. _statsd: https://github.com/statsd/statsd
.. _python-statsd: https://statsd.readthedocs.io/
.. _StatsClient: https://statsd.readthedocs.io/en/latest/configure.html
.. _Notifiers: https://github.com/notifiers/notifiers
.. _Notifiers Providers docs: https://notifiers.readthedocs.io/en/latest/providers/index.html
.. _NotificationHandler: https://notifiers.readthedocs.io/en/latest/api/core.html#notifiers.logging.NotificationHandler
.. _configure: https://loguru.readthedocs.io/en/stable/overview.html?highlight=configure#suitable-for-scripts-and-libraries
.. _environment variables: https://loguru.readthedocs.io/en/stable/api/logger.html#env
