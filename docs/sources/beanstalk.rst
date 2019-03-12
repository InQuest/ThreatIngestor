.. _beanstalk-source:

Beanstalk
---------

The **Beanstalk** source can be used to read content from `Beanstalk`_ queues.
This, combined with the :ref:`Beanstalk Operator <beanstalk-operator>`, allows
a :ref:`full-circle workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``beanstalk``
* ``paths`` (required): A list of XPath-like_ expressions representing the JSON fields you want to extract from.
* ``reference``: An XPath-like_ expression representing the JSON field you want to use as a reference. (default: source name).
* ``host`` (required): Host to connect to.
* ``port`` (required): Port to connect over.
* ``queue_name`` (required): The name of the Beanstalk queue you want to use.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: beanstalk-input
      module: beanstalk
      paths: [content]
      reference: reference
      host: 127.0.0.1
      port: 11300
      queue_name: MYQUEUENAME

If you are expecting JSON jobs in the Beanstalk queue that look like this:

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

.. _Beanstalk: https://beanstalkd.github.io/
.. _XPath-like: https://github.com/kennknowles/python-jsonpath-rw
