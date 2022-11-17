.. _github-gist-source:

GitHub Gist Username Search
------------------------

The **GitHub Gist** source plugin uses GitHub's `gist API`_ to find new gists created by a user, and create a :ref:`Task artifact <task-artifact>` for each.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``github-gist``
* ``user`` (required): Username of the gist owner.
* ``username`` (optional): Username for authentication.
* ``token`` (optional): Token or password for authentication.

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

    - name: github-gist-search
      credentials: github-auth
      module: github-gist
      user: Hifumi1337

.. _github gist user API: https://docs.github.com/en/rest/gists/gists#list-gists-for-a-user
