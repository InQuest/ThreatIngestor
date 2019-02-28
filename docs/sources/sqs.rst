SQS
---

The **SQS** source can be used to read content from `Amazon SQS`_ queues. This,
combined with the :ref:`SQS Operator <sqs-operator>`, allows a :ref:`full-circle
workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sqs``
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
      credentials: aws-auth
      queue_name: MYQUEUENAME

.. _Amazon SQS: https://aws.amazon.com/sqs/
