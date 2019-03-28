.. _installation:

Installation
============

ThreatIngestor requires Python 3.6+.

You may need to install the Python development headers seperately. On Ubuntu/Debian-based systems, try::

    sudo apt-get install python3-dev

Then install ``threatingestor`` from pip::

    pip install threatingestor

By default, threatingestor does not pull all dependencies for plugins you may not use. If you want to use a certain plugin, you'll need to pull in its dependencies as well. For example, if you want to use SQS queues::

    pip install threatingestor[sqs]

If you want to use Beanstalk and Twitter::

    pip install threatingestor[beanstalk,twitter]

Or if you don't know what you might need, and want to just pull in everything::

    pip install threatingestor[all]

.. note::

    If you'd like to use the ``git`` source, you will also need to have Git installed.

    If you want to use the notification support, install Notifiers separately: ``pip install notifiers``.
