Extras
======

There are a few extra tools included alongside ThreatIngestor, that didn't quite make sense as sources or operators.

BugSnag
-------

BugSnag monitoring is a valuable tool to have when running in daemon mode. Adding it is extremely simple and the only requirement is to have an API key.

Here's an example to include in your ``config.yml``:

.. code-block:: yaml

    error_reporting:
      - name: bugsnag
        api_key: API_KEY

Quick Webapp
------------

The first tool is the tiny ThreatIngestor webapp, described in the :ref:`Try it out! <try-it-out>` section. This simple app provides a JSON API, and a couple HTML pages with a dynamic table of artifacts. Use this to get a quick overview of artifacts being sent through a :ref:`SQLite operator <sqlite-operator>`.

The webapp requires an artifacts database created by the SQLite operator, with the name ``artifacts.db``, in the working directory.

Queue Workers
-------------

Included in the ``extras`` package is a base class for creating :ref:`Queue Workers <queue-worker-workflow>`. Two example workers are provided: ``FSWatcher`` and ``PasteProcessor``.

Queue workers can use any supported queue system for input and/or output: currently, SQS and Beanstalk. They are expected to read from a YAML config file, which looks similar to ThreatIngestor's own YAML config.

See the :py:mod:`QueueWorker API docs <threatingestor.extras.queueworker>` for more information on creating custom Queue Workers.

FSWatcher
~~~~~~~~~

The "file system watcher" queue worker can be set to watch a configured directory for new and modified YARA rules, and notify a queue with the contents of the rules.

Example Configuration
^^^^^^^^^^^^^^^^^^^^^

Here's an example YAML config file using SQS, writing to the ``yara-rules`` queue:

.. code-block:: yaml

    module: sqs
    aws_access_key_id: MYKEY
    aws_secret_access_key: MYSECRET
    aws_region: MYREGION
    out_queue: yara-rules
    watch_path: MY_RULES_FOLDER

Note that FSWatcher doesn't use an ``in_queue``, since its input comes from the file system changes themselves.

Example Usage
^^^^^^^^^^^^^

.. code-block:: sh

    python3 -m threatingestor.extras.fswatcher fswatcher.yml

Expected Results
^^^^^^^^^^^^^^^^

When you change or create rule files, FSWatcher should detect those changes and send the contents of the rules to the queue, with a JSON message like this:

.. code-block:: json

    {
        "rules": "rule myNewRule { condition: false }",
        "filename": "mynewrule.yara"
    }

PasteProcessor
~~~~~~~~~~~~~~

The "paste processor" queue worker will watch a configured input queue for URLs, attempt to fetch the "raw" contents if the URL appears to be a "pastebin" link, and send those contents to a configured output queue. This can be useful if you have, for example, a :ref:`Twitter source <twitter-source>` that finds "pastebin.com" links full of :term:`IOCs <IOC>`, and you want to extract those IOCs from the paste.

.. note::

    The name is slightly misleading - if URLs sent to the PasteProcessor don't appear to be pastebin links, they will still be processed. The contents of the provided URL will be sent to the output queue.

Example Configuration
^^^^^^^^^^^^^^^^^^^^^

Here's an example YAML config file using Beanstalk, reading from the ``pastebin-processor`` tube and writing to the ``threatingestor-input`` tube:

.. code-block:: yaml

    module: beanstalk
    host: localhost
    port: 11300
    in_queue: pastebin-processor
    out_queue: threatingestor-input

Here, you would want a ThreatIngestor operator writing to the ``pastebin-processor`` tube, and a ThreatIngestor source reading from the ``threatingestor-input`` tube.

Example Usage
^^^^^^^^^^^^^

.. code-block:: sh

    python3 -m threatingestor.extras.pasteprocessor pasteprocessor.yml

Expected Results
^^^^^^^^^^^^^^^^

When you (or ThreatIngestor) send JSON jobs to the ``pastebin-processor`` queue that look like this:

.. code-block:: json

    {
        "url": "https://pastebin.com/EXAMPLE"
    }

PasteProcessor will kick off and send you back the contents of that paste, in the ``threatingestor-input`` tube:

.. code-block:: json

    {
        "content": "EXAMPLE TEXT",
        "reference": "https://pastebin.com/raw/EXAMPLE"
    }
