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
* ``filename`` (required): filename with relative or absolute path.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: mycsv
      module: csv
      filename: output.csv
