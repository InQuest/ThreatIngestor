.. _beanstalk-operator:

Beanstalk
---------

Beanstalk_ is a simple work queue server, that may be easier to get started
with than Amazon SQS for those who don't already have AWS accounts.

The Beanstalk operator enables you to send output to work queues, which you can
then consume from :ref:`Beanstalk sources <beanstalk-source>`, or external
applications. This operator is extremely flexible, as it accepts arbitrary
config options and passes them through to the queue.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``beanstalk``
* ``host`` (required): Host to connect to.
* ``port`` (required): Port to connect over.
* ``queue_name`` (required): The name of the Beanstalk tube you want to use.

Any other options defined in the Beanstalk operator section will be passed in to
your queue as part of a JSON object, after string interpolation to fill in
artifact content. For example, ``{domain}`` will be replaced with the C2 domain
being exported.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: my-beanstalk-queue
      module: beanstalk
      host: 127.0.0.1
      port: 11300
      queue_name: my-queue
      domain: {domain}
      url: {url}
      source_type: url
      download_path: /data/ingestor

In this example, the resulting JSON object for a URL artifact of
``http://example.com/`` sent to the Beanstalk queue would be:

.. code-block:: json

    {
        "domain": "example.com",
        "url": "http://example.com/",
        "source_type": "url",
        "download_path": "/data/ingestor"
    }

.. _Beanstalk: https://beanstalkd.github.io/
