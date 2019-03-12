.. _artifacts:

Artifacts
=========

At the core of ThreatIngestor is the Artifact system. Sources create Artifacts, and Operators operate on Artifacts.

Each configured :ref:`source <source-plugins>` will run content through iocextract_, along with some pre-processing depending on the source. (E.g., the RSS source removes some HTML tags to produce better results.) Additional artifacts, such as "Tasks", may also be created.

Extracted artifacts are then returned from the sources, and passed along to operators as one of the supported **Artifact** classes below. Based on your configuration, operators decide how to handle each artifact based on its type and any configured :ref:`filters <operator-plugins>`.

All artifacts are context-aware, meaning they keep track of where and why they were created. By default, they have a "Reference Link," a "Reference Text", and the name of the Source that created them. Depending on the Artifact type, they may also have additional context: **URL** Artifacts know whether they link to domains or IP addresses, and what that domain or IP is; **IPAddress** Artifacts know whether they are IPv4 or IPv6; all network Artifacts (URL, Domain, IPAddress) know whether they are "defanged". For complete documentation on each Artifact type, see below.

.. note::

    For documentation on context available to every Artifact regardless of type, see the :py:mod:`Artifact API Documentation <threatingestor.artifacts.Artifact.format_message>`.

.. _domain-artifact:

Domains
-------

In ThreatIngestor terms, domains are a subset of URLs where the network location portion of the URL is a FQDN, not an IP address. ThreatIngestor does not do any verification of TLDs, nor does it attempt to extract domains directly from source text, due to an extremely high false positive rate. If you find that valid C2 domains in one of your sources are being passed over because they aren't extracted by the URL regex, you should consider using a :ref:`Task <task-artifact>` artifact to manually find those C2s.

For information on available context for Domain artifacts, see the :py:mod:`Domain API Documentation <threatingestor.artifacts.Domain.format_message>`.

.. _hash-artifact:

Hashes
------

The following hash types will be extracted from all sources:

* MD5
* SHA1
* SHA256
* SHA512

For information on available context for Hash artifacts, see the :py:mod:`Hash API Documentation <threatingestor.artifacts.Hash.format_message>`.

.. _ipaddress-artifact:

IP Addresses
------------

ThreatIngestor supports IPv4 and IPv6 addresses, including "defanged" IPs.

.. note::

   When extracting from a ``Source``, IP addresses designated as private (e.g. ``192.168.0.1``), loopback (e.g. ``127.0.0.1``), or reserved (e.g. ``198.51.100.1``) are automatically excluded from the results.

For information on available context for IPAddress artifacts, see the :py:mod:`IPAddress API Documentation <threatingestor.artifacts.IPAddress.format_message>`.

.. _task-artifact:

Tasks
-----

Tasks are a sort of catchall artifact useful for queuing up manual work for analysts. How they are generated is up to the individual source plugin. The Twitter source, for example, will generate a single Task artifact for each tweet it processes. You can then configure your operator plugins to use or ignore Task artifacts, as appropriate.

Consider the common case of a blog post from **Vendor X** where IOCs are publicly shared, but are unfortunately embedded in a PDF attached to the post rather than plaintext in the RSS feed itself. Configure your ThreatIngestor sources and operators to add a Task artifact every time **Vendor X** makes a new post. When an analyst sees the Task, they can follow the reference link, manually extract any new IOCs, and go on with their work.

For information on available context for Task artifacts, see the `Task API Documentation <threatingestor.artifacts.Task.format_message>`.

.. _url-artifact:

URLs
----

ThreatIngestor will extract URLs using iocextract_'s extraction rules, including "defanged" URLs.

For information on available context for URL artifacts, see the :py:mod:`URL API Documentation <threatingestor.artifacts.URL.format_message>`.

URLs have access to additional :ref:`filters <operator-plugins>` that can be used in operator configuration. See the :py:mod:`URL API Documentation (match function) <threatingestor.artifacts.URL.match>` for more information.

.. _yarasignature-artifact:

YARA Signatures
---------------

Full YARA signatures will automatically be extracted from all sources.

For information on available context for YARASignature artifacts, see the :py:mod:`YARASignature API Documentation <threatingestor.artifacts.YARASignature.format_message>`.

.. _iocextract: https://iocextract.readthedocs.io/en/latest/
