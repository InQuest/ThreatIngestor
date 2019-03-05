.. _source-plugins:

Source Plugins
==============

For each source specified, ``ThreatIngestor`` handles artifact import. Sources may link to Twitter, Blogs, etc. Artifacts are imported from those sources and could include URLs, IP Addresses, YARA Signatures, etc. All source plugins maintain state between runs, allowing them to skip previously processed artifacts and get right to work finding new indicators.

To add a source to your configuration file, include a section like this:

.. code-block:: yaml

    sources:
      - name: mysource
        module:  mysourcemodule

You can add as many sources as you need, all under the same ``sources:`` list.

.. code-block:: yaml

    sources:
      - name: mysource
        module: mysourcemodule

      - name: myothersource
        module: mysourcemodule

Note the use of dashes to signify the start of each item in the list, and matching indentation for all the keys within each item.

The ``module`` option must match one of the sources listed below, or your :ref:`custom source <custom-source-plugins>`. The ``name`` is freeform.

All sources allow credentials such as usernames, passwords, OAuth tokens, etc to be defined in a seperate ``credentials`` section and referenced by name with a ``credentials`` keyword. Consider a plugin that accepts a ``token`` and a ``secret``. In ``config.yml``, you would set it up the ``credentials`` and ``sources`` sections like this:

.. code-block:: yaml

    credentials:
      - name: mysource-auth
        token: MYTOKEN
        secret: MYSECRET

    sources:
      - name: mysource
        credentials: mysource-auth

This allows the same credentials to be reused for several different sources (or operators) without having to duplicate them in each source definition.

Available Plugins
-----------------

The available source plugins are:

.. toctree::
   :maxdepth: 1
   :glob:

   sources/*
