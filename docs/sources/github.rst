.. _github-source:

GitHub Repository Search
------------------------

The **GitHub** source plugin uses GitHub's `repository search API`_ to find new
interesting repos, and create a :ref:`Task artifact <task-artifact>` for each.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``github``
* ``search`` (required): search term(s).
* ``username``: Optional username for authentication.
* ``token``: Optional token or password for authentication.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

The following examples all assume GitHub credentials have already been
configured in the ``credentials`` section of the config, like this:

.. code-block:: yaml

    credentials:
      - name: github-auth
        username: myuser
        token: MYTOKEN

.. note::

    GitHub credentials are optional, but increase the rate limit for API
    requests *significantly*. If you are doing more than one or two low-
    volume searches, you should set up the credentials.

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: github-cve-repos
      credentials: github-auth
      module: github
      search: CVE-2018-

.. _repository search API: https://developer.github.com/v3/search/#search-repositories
