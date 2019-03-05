.. _glossary:

Glossary
========

Commonly used terms and their definitions.

.. glossary::

    Artifact
        Used throughout ThreatIngestor to describe a single, specific piece of :term:`Threat Intelligence`, such as a domain or file hash.

    C2
        Also known as "C&C" or "Command and Control," C2 domains and IP addresses are a form of :term:`IOC` that describe the infrastructure of a malicious actor. Malware typically "phones home" to these C2s in order to exfiltrate information or receive commands from the malicious actor.

    Defanged
        An :term:`IOC` that has been modified in some way to prevent accidental exposure to malicious content, or to avoid being marked as malicious by an antivirus or other security system. Analysts oftem "defang" IOCs before sharing them publicly. Common defangs include replacing "http" with "hxxp", or "." with "[.]" to disable links, e.g.: ``http://example[.]com``.

    IOC
        `Indicator of Compromise`_: a piece of information that shows evidence of a malicious actor, such as a file hash for a piece of malware, or a domain used as a :term:`C2`. See also :term:`Threat Intelligence`.

    OSINT
        Open Source Intelligence: publicly available information used in an intelligence context; see also :term:`Threat Intelligence`.

    Threat Intelligence
        Information that describes the capabilities, characteristics, infrastructure, etc of a given "threat," usually malicious software or malicious actors. This can include :term:`C2` domains and IP addresses, SSL certificates, :term:`YARA` rules, file hashes, and more.

    YARA
        A tool used widely by malware analysts to identify and classify malware. See `virustotal.github.io/yara/`_. YARA "rules" are often shared between analysts to help others detect a certain piece of malware.


.. _virustotal.github.io/yara/: https://virustotal.github.io/yara/
.. _Indicator of Compromise: https://en.wikipedia.org/wiki/Indicator_of_compromise
