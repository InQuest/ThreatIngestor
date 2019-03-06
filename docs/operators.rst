.. _operator-plugins:

Operator Plugins
================

Operator plugins handle artifact export. They can be configured to only send certain artifact types, only send artifacts from certain sources, filter down artifacts to only those matching a certain regex, and more.

To add an operator to your configuration file, include a section like this:

.. code-block:: yaml

    operators:
      - name: myoperator
        module: myoperatormodule

The ``module`` option must match one of the operators listed below, or your :ref:`custom operator <custom-operator-plugins>`.

The following options are globally accepted by all operators:

* ``allowed_sources``: List (`in YAML syntax`_) of source names to allow.
* ``artifact_types``: List (`in YAML syntax`_) of artifact types to allow.
* ``filter``: A regex, or **comma-separated list** (*not* in YAML syntax) of some :py:mod:`special keywords <threatingestor.artifacts.URL.match>`.

All of these options are *inclusive*, so only artifacts matching the restrictions will be sent through the operator.

Example:

.. code-block:: yaml

    sources:
      - name: mysource
        module: mysourcemodule

      - name: myothersource
        module: mysourcemodule

    operators:
      - name: non-ip-based-urls
        module: myoperatormodule
        allowed_sources: [mysource]
        filter: is_domain
        artifact_types: [URL]

      - name: google-domain-masquerade
        module: myoperatormodule
        allowed_sources: [mysource, myothersource]
        filter: ([^\.]google.com$|google.com[^/])
        artifact_types: [URL, Domain]

By combining these three options, you can include any number of different sources and operators in your config, and still only send exactly the artifacts you want to each operator.

All operators allow credentials such as usernames, passwords, OAuth tokens, etc to be defined in a seperate ``credentials`` section and referenced by name with a ``credentials`` keyword. Consider a plugin that accepts a ``token`` and a ``secret``. In ``config.yml``, you would set it up the ``credentials`` and ``operators`` sections like this:

.. code-block:: yaml

    credentials:
      - name: myoperator-auth
        token: MYTOKEN
        secret: MYSECRET

    operators:
      - name: myoperator
        credentials: myoperator-auth

This allows the same credentials to be reused for several different operators (or sources), without having to duplicate them in each operator definition.


Available Plugins
-----------------

The available operator plugins are:

.. toctree::
   :maxdepth: 1
   :glob:

   operators/*

.. _in YAML syntax: https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html
