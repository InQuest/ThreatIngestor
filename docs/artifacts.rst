.. _artifacts:

Artifacts
=========

Each configured :ref:`source <source_plugins>` will be run through
:ref:`iocextract <iocextract>`, along with some pre-processing depending on the
source. (E.g., the RSS source removes some HTML tags to produce better results.)

Extracted IOCs are then returned from the sources, and passed along to
operators as one of the supported **Artifact** classes below. Based on your
configuration, operators decide how to handle each artifact based on its type
and any configured :ref:`filters <filters>`.

.. _ipaddress-artifact:

IP Addresses
------------

ThreatIngestor supports IPv4 and IPv6 addresses, including "defanged" IPs.

.. _url-artifact:

URLs
----

ThreatIngestor will extract URLs using `iocextract`'s extraction rules,
including "defanged" URLs. 

.. _domain-artifact:

Domains
-------

In ThreatIngestor terms, domains are a subset of URLs where the network
location portion of the URL is a FQDN, not an IP address. ThreatIngestor does
not do any verification of TLDs, nor does it attempt to extract domains
directly from source text, due to an extremely high false positive rate. If you
find that valid C2 domains in one of your sources are being passed over because
they aren't extracted by the URL regex, you should consider using a :ref:`Task
<task-artifact>` artifact to manually find those C2s.

.. _yarasignature-artifact:

YARA Signatures
---------------

Full YARA signatures will automatically be extracted from all sources.

.. _hash-artifact:

Hashes
------

The following hash types will be extracted from all sources:

* MD5
* SHA1
* SHA256
* SHA512

.. _task-artifact:

Tasks
-----

Tasks are a sort of catchall artifact useful for queuing up manual work for
analysts. How they are generated is up to the individual source plugin. The
Twitter source, for example, will generate a single Task artifact for each
tweet it processes. You can then configure your operator plugins to use or
ignore Task artifacts, as appropriate.

Consider the common case of a blog post from **Vendor X** where IOCs are
publicly shared, but are unfortunately embedded in a PDF attached to the post
rather than plaintext in the RSS feed itself. Configure your ThreatIngestor
sources and operators to add a Task artifact every time **Vendor X** makes a
new post. When an analyst sees the Task, they can follow the reference link,
manually extract any new IOCs, and go on with their work.
