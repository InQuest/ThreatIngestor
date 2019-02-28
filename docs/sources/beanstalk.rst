.. _beanstalk-source:

Beanstalk
---------

The **Beanstalk** source can be used to read content from `Beanstalk`_ queues.
This, combined with the :ref:`Beanstalk Operator <beanstalk-operator>`, allows
a :ref:`full-circle workflow <full-circle-workflow>`.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``beanstalk``
* ``host`` (required): Host to connect to.
* ``port`` (required): Port to connect over.
* ``queue_name`` (required): The name of the Beanstalk queue you want to use.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: beanstalk-input
      module: beanstalk
      host: 127.0.0.1
      port: 11300
      queue_name: MYQUEUENAME

.. _Beanstalk: https://beanstalkd.github.io/
