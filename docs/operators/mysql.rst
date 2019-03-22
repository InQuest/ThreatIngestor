.. _mysql-operator:

MySQL
-----

The MySQL operator feeds artifacts into a single MySQL table.

The table defined in the config will be created if it does not exist. The columns in the table are:

1. ``artifact``: Artifact content (``example.com``, ``1.1.1.1``, etc).
1. ``artifact_type``: Artifact type (``domain``, ``yarasignature``, etc).
2. ``reference_link``: URL of the source tweet, blog post, etc.
3. ``reference_text``: Tweet text, snippet from a blog post, etc.
4. ``created_date``: MySQL DATETIME.
5. ``state``: For external use, always ``NULL``. You can use this to keep track of the current investigation status of artifacts, if you so choose.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``mysql``
* ``host`` (required): Database host.
* ``port``: Database port (default: 3306).
* ``user`` (required): Database user (must have table create permission, or insert permission on the existing artifacts table defined below).
* ``password``: Password for ``user``.
* ``table`` (required): Artifacts table (will be created if it does not exist; must follow the required schema).

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following example assumes MySQL credentials have already been configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: mysql-auth
        host: MYHOST
        port: MYPORT
        user: MYUSER
        password: MYPASSWORD
        database: MYDATABASE

Inside the ``operators`` section of your configuration file:

.. code-block:: yaml

    - name: my-db
      module: mysql
      credentials: mysql-auth
      table: artifacts
