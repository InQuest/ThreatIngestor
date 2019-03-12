.. _misp-operator:

MISP
----

The MISP operator will send extracted artifacts to your MISP_ instance, as
objects attached to events.

When this plugin is configured, events should show up on your MISP instance
with the name "ThreatIngestor Event: {SOURCE}", where "{SOURCE}" is the name of
the source plugin that extracted the attached objects. Artifact context
(reference link and text, if any) will also be attached to the event, as
"internal" objects.

The following artifacts are supported by the MISP plugin:

* Domains
* Hashes (MD5, SHA1, SHA256)
* IP Addresses
* URLs
* YARA Signatures

If other artifact types are sent through this plugin, the artifacts will be
ignored.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``misp``
* ``url`` (required): Base URL for your MISP instance.
* ``secret_key`` (required): Your MISP authentication key.
* ``ssl``: Verify SSL certificate? (default: true)
* ``tags``: List of tags to attach to events (default: ``[type:OSINT]``)

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following example assumes MISP credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: misp-auth
        url: http://mymisp
        key: MYKEY
        ssl: false

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: mymisp
      module: misp
      credentials: misp-auth

.. _MISP: https://www.misp-project.org/
