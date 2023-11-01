.. _sitemap-source:

Sitemap Parser
--------------

The **Sitemap** source plugin parses the ``/sitemap.xml`` file to locate all blogs associated with that specific domain.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``sitemap``
* ``url`` (required): URL of the website with the sitemap path.
* ``include`` (optional): Include filter using simplified regex.
* ``exclude`` (optional): Exclude filter using raw regex.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Quick setup for sitemap parsing:

.. code-block:: yaml

    - name: inquest-blog
      module: sitemap
      url: https://inquest.net/sitemap.xml
      include: security|threat|research
      exclude: https:\/.inquest\.net\/blog[\/]?inquest-[\/]?
