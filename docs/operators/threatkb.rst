.. _threatkb-operator:

ThreatKB
--------

The ThreatKB operator will send extracted artifacts to your ThreatKB_
instance.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``threatkb``
* ``url`` (required): Base URL for your ThreatKB instance.
* ``token`` (required): Your ThreatKB authentication token.
* ``secret_key`` (required): Your ThreatKB authentication secret key.
* ``state`` (required): The State you want assigned to created artifacts.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following example assumes ThreatKB credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: threatkb-auth
        url: http://mythreatkb
        token: MYTOKEN
        secret_key: MYKEY

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: mythreatkb
      module: threatkb
      credentials: threatkb-auth
      state: Inbox

.. _ThreatKB: https://github.com/InQuest/ThreatKB
