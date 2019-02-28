.. _git-source:

Git
---

The first time it's run, each **Git** source will clone the configured
repository, look for any files matching ``*.{rule,rules,yar,yara}``, and
extract YARA rules. On any subsequent runs, it will run ``git pull``, check for
new and updated files matching the same patterns, and extract YARA rules from
those files.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

* ``module`` (required): ``git``
* ``url`` (required): URL (can be https, git, ssh, etc) of remote to clone.
* ``local_path`` (required): folder on disk (relative or absolute) to clone into.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

Inside the ``sources`` section of your configuration file:

.. code-block:: yaml

    - name: inquest-yara-rules
      module: git
      url: https://github.com/InQuest/yara-rules.git
      local_path: /opt/threatingestor/git/yara-rules

