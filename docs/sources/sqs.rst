SQS
---

The **SQS** source can be used to read content from `Amazon SQS`_ queues. This,
combined with the :ref:`SQS Operator <sqs-operator>`, allows a :ref:`full-circle
workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sqs``
* ``paths`` (required): A list of XPath-like_ expressions representing the JSON fields you want to extract from.
* ``reference``: An XPath-like_ expression representing the JSON field you want to use as a reference. (default: source name).
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
      paths: [content]
      reference: reference
      credentials: aws-auth
      queue_name: MYQUEUENAME

If you are expecting JSON jobs in the SQS queue that look like this:

.. code-block:: json

    {
        "content": "freeform text",
        "reference": "http://example.com"
    }

The above config will extract artifacts from the value of the ``content`` key, and use the value of the ``reference`` key as the artifact's reference.

If you instead had JSON jobs like this:

.. code-block:: json

    {
        "data": {
            "text": "freeform text",
            "more": "more text",
            "ref": "http://example.com"
        }
    }

And you want to extract from ``text`` and ``more``, with ``ref`` as a reference, you could set up your config to account for the more complex JSON structure:

.. code-block:: yaml

      paths: [data.text, data.more]
      reference: data.ref

This flexibility allows easier integration with arbitrary systems.

.. _Amazon SQS: https://aws.amazon.com/sqs/
.. _XPath-like: https://github.com/kennknowles/python-jsonpath-rw
