.. _sqs-operator:

Amazon SQS
----------

The SQS_ operator allows ThreatIngestor to integrate out-of-the-box with any
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

.. _SQS: https://aws.amazon.com/sqs/
