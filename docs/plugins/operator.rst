.. _operator-plugins:

Operator Plugins
================

Operator plugins handle artifact export. They can be configured to only send
certain artifact types, only send artifacts from certain sources, filter down
artifacts to only those matching a certain regex, and more.

To add an operator to your configuration file, include a section like this:

.. code-block:: yaml

    operators:
      - name: myoperator
        module: myoperatormodule

The ``module`` option must match one of the operators listed below, or your
:ref:`custom operator <custom-operator-plugins>`.

The following options are globally accepted by all operators:

* ``allowed_sources``: List (`in YAML syntax`_) of source names to allow.
* ``artifact_types``: List (`in YAML syntax`_) of artifact types to allow.
* ``filter``: A regex, or **comma-separated list** (*not* in YAML syntax)
  of some `special keywords <../api.html#threatingestor.artifacts.URL.match>`_.

All of these options are *inclusive*, so only artifacts matching the
restrictions will be sent through the operator.

Example: 

.. code-block:: yaml

    sources:
      - name: mysource
        module: mysourcemodule

      - name: myothersource
        module: mysourcemodule

    operators:
      - name: non-ip-based-urls
        module: myoperatormodule
        allowed_sources: [mysource]
        filter: is_domain
        artifact_types: [URL]

      - name: google-domain-masquerade
        module: myoperatormodule
        allowed_sources: [mysource, myothersource]
        filter: ([^\.]google.com$|google.com[^/])
        artifact_types: [URL, Domain]

By combining these three options, you can include any number of different
sources and operators in your config, and still only send exactly the artifacts
you want to each operator.

All operators allow credentials such as usernames, passwords, OAuth tokens, etc
to be defined in a seperate ``credentials`` section and referenced by name with
a ``credentials`` keyword. Consider a plugin that accepts a ``token`` and a
``secret``. In ``config.yml``, you would set it up the ``credentials`` and
``operators`` sections like this:

.. code-block:: yaml

    credentials:
      - name: myoperator-auth
        token: MYTOKEN
        secret: MYSECRET

    operators:
      - name: myoperator
        credentials: myoperator-auth

This allows the same credentials to be reused for several different operators
(or sources), without having to duplicate them in each operator definition.

.. _csv-operator:

CSV File
--------

The most basic of the included operators, the CSV operator simply writes
extracted artifacts to a CSV file. The columns in the file are, in order:

1. Artifact type (``URL``, ``Domain``, ``IPAddress``, etc)
2. Artifact content (``example.com``, ``1.1.1.1``)
3. Reference link (URL of the source tweet, blog post, etc)
4. Reference text (Tweet text, snippet from a blog post, etc)

This operator often comes in handy if you want to quickly and easily test
your ThreatIngestor configuration is working as expected.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``csv``
* ``filename`` (required): filename with relative or absolute path.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: mycsv
      module: csv
      filename: output.csv

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

.. _sqs-operator:

Amazon SQS
----------

The SQS operator allows ThreatIngestor to integrate out-of-the-box with any
system that supports reading from SQS queues. This operator is extremely
flexible, as it accepts arbitrary config options and passes them through
to the queue.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sqs``
* ``aws_access_key_id`` (required): Your AWS access key ID.
* ``aws_secret_access_key`` (required): Your AWS secret access key.
* ``aws_region`` (required): Your AWS region name.
* ``queue_name`` (required): The name of the SQS queue you want to use.

Any other options defined in the SQS operator section will be passed in to your
queue as part of a JSON object, after string interpolation to fill in artifact
content. For example, ``{domain}`` will be replaced with the C2 domain being
exported.

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

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: myqueue
      module: sqs
      credentials: aws-auth
      queue_name: my-queue
      domain: {domain}
      url: {url}
      source_type: url
      download_path: /data/ingestor

In this example, the resulting JSON object for a URL artifact of
``http://example.com/`` sent to the SQS queue would be:

.. code-block:: json

    {
        "domain": "example.com",
        "url": "http://example.com/",
        "source_type": "url",
        "download_path": "/data/ingestor"
    }

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

.. _ThreatKB: https://github.com/InQuest/ThreatKB
.. _Twitter oauth docs: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
.. _in YAML syntax: https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html
