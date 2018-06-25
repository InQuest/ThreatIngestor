.. _operator-plugins:

Operator Plugins
================

Operator plugins handle artifact export. They can be configured to only send
certain artifact types, only send artifacts from certain sources, filter down
artifacts to only those matching a certain regex, and more.

To add an operator to your configuration file, include a section like this:

.. code-block:: ini

    [operator:myoperator]
    module = myoperatormodule

ThreatIngestor looks for sections matching ``operator:``, and uses the rest
of the section name as the operator name. The ``module`` option must match
one of the operators listed below, or your :ref:`custom operator
<custom-operator-plugins>`.

The following options are globally accepted by all operators:

* ``allowed_sources``: Comma-separated list of source names to allow
* ``artifact_types``: Comma-separated list of artifact types to allow
* ``filter``: A regex, or comma-separated list of some `special keywords`

All of these options are *inclusive*, so only artifacts matching the
restrictions will be sent through the operator.

Example: 

.. code-block:: ini

    [source:mysource]
    module = mysourcemodule

    [source:myothersource]
    module = mysourcemodule

    [operator:non-ip-based-urls]
    module = myoperatormodule
    allowed_sources = mysource
    filter = is_domain
    artifact_types = URL

    [operator:google-domain-masquerade]
    module = myoperatormodule
    allowed_sources = mysource, myothersource
    filter = ([^\.]google.com$|google.com[^/])
    artifact_types = URL, Domain

By combining these three options, you can include any number of different
sources and operators in your config, and still only send exactly the artifacts
you want to each operator.

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
* ``filename`` (required): filename with relative or absolute path

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [operator:mycsv]
    module = csv
    filename = output.csv

.. _threatkb-operator:

ThreatKB
--------

The ThreatKB operator will send extracted artifacts to your ThreatKB_
instance.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``threatkb``
* ``url`` (required): Base URL for your ThreatKB instance
* ``token`` (required): Your ThreatKB authentication token
* ``secret_key`` (required): Your ThreatKB authentication secret key
* ``state`` (required): The State you want assigned to created artifacts

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [operator:mythreatkb]
    module = threatkb
    url = http://mythreatkb
    token = MYTOKEN
    secret_key = MYKEY
    state = Inbox

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
* ``aws_access_key_id`` (required): Your AWS access key ID
* ``aws_secret_access_key`` (required): Your AWS secret access key
* ``aws_region`` (required): Your AWS region name
* ``queue_name`` (required): The name of the SQS queue you want to use

Any other options defined in the SQS operator section will be passed in to your
queue as part of a JSON object, after string interpolation to fill in artifact
content. For example, ``{domain}`` will be replaced with the C2 domain being
exported.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    [operator:myqueue]
    module = sqs
    aws_access_key_id = MY_KEY
    aws_secret_access_key = MY_SECRET
    aws_region = my-region
    queue_name = my-queue
    domain = {domain}
    url = {url}
    source_type = url
    download_path = /data/ingestor

In this example, the resulting JSON object for a URL artifact of
``http://example.com/`` sent to the SQS queue would be:

.. code-block:: json

    {
        "domain": "example.com",
        "url": "http://example.com/",
        "source_type": "url",
        "download_path": "/data/ingestor"
    }

.. _ThreatKB: https://github.com/InQuest/ThreatKB
