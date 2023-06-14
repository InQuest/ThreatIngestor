.. _virustotal-source:

VirusTotal
----------

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``virustotal``
* ``user`` (required): Author of the comments.
* ``api_key`` (required): Consumer API key.
* ``limit`` (optional): Set a limit for how many VirusTotal comments are ingested (default is 10).

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

First, add your VirusTotal API key under the ``credentials`` section:

.. code-block:: yaml

    - name: virustotal-auth
      api_key: API_KEY


Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: vt-comments-inquest
      module: virustotal
      user: 'inquest.labs'
      credentials: virustotal-auth
      limit: 12
