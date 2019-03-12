.. _sqlite-operator:

SQLite
------

The SQLite operator feeds artifacts into a simple database, with zero setup
required.

This operator often comes in handy if you want to quickly and easily test
your ThreatIngestor configuration is working as expected, but scales better
than the CSV operator.

One table will be created per artifact type. The columns in each table are, in
order:

1. ``artifact``: Artifact content (``example.com``, ``1.1.1.1``, etc).
2. ``reference_link``: URL of the source tweet, blog post, etc.
3. ``reference_text``: Tweet text, snippet from a blog post, etc.
4. ``created_date``: ISO-8601 date string, always UTC.
5. ``state``: For external use, always ``NULL``. You can use this to keep track
   of the current investigation status of artifacts, if you so choose.

You can also use the included ThreatIngestor "quick web interface" to get an
easier overview of the artifacts in your database, or set up a JSON API with
a single command::

    hug -m threatingestor.extras.webapp

.. note::

    Don't have hug? ``pip install hug``!

If you want to use the webapp, make sure your SQLite database is called
``artifacts.db`` and in the same folder where you're running ``hug``.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sqlite``
* ``filename`` (required): filename with relative or absolute path.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: mysqlite
      module: sqlite
      filename: output.db
