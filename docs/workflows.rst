.. _example-workflows:

Example Workflows
=================

The :ref:`standard use case <standard-case>` for ThreatIngestor is pretty
simple - just pull from Twitter and RSS, extract IOCs, and send them to
ThreatKB. That said, there is a *lot* more you can do with just a few changes
to the configuration file. Here, we'll go over some more advanced use cases,
to give you an idea what this tool can do.

.. _multiple-operator-workflow:

Multiple Operators
------------------

By adding more than one operator, you can tell ThreatIngestor to send artifacts
to multiple locations. This might be useful if you want to send to ThreatKB
while also writing out a local log file. Combine this with a few :ref:`operator
options <operator-plugins>` though, and you can now send *specific* artifacts
to different operators depending on type, source, or advanced filters. Consider
the following workflow:

.. image:: _static/mermaid-multiple-operators.png
   :align: center
   :alt: Flowchart with five inputs on the left, all feeding into
         ThreatIngestor in the center, which in turn feeds into three
         outputs on the right. The inputs are "Twitter C2 List," "Twitter
         Search: #opendir," "Twitter Search: virustotal.com," "Vendor X Blog,"
         and "Domain Masquerade Feed." The outputs are "ThreatKB," "Crawler,"
         and "Automated Analysis."

We want artifacts from "Twitter C2 List" and "Vendor X Blog" to go directly to
ThreatKB. URLs and domains from "Twitter Search: #opendir" and "Domain
Masquerade Feed" should go to our crawler, which will look for malicious
content or evidence of phishing attacks. Any URLs from "Twitter Search:
virustotal.com" that match the filter for a direct URL to a sample should be
sent to our "Automated Analysis" system, which will log in to VirusTotal,
download the sample, and analyze it. We don't want to see VirusTotal links or
open directories in ThreatKB though, because those aren't C2s. This config
accomplishes all of that:

.. code-block:: yaml

    general:
        daemon: true
        sleep: 900
        state_path: state.db

    credentials:
      - name: twitter-auth
        token: MYTOKEN
        token_key: MYKEY
        con_secret_key: MYSECRETKEY
        con_secret: MYSECRET

      - name: threatkb-auth
        url: http://mythreatkb
        token: MYTOKEN
        secret_key: MYKEY

      - name: aws-auth
        aws_access_key_id: MYKEY
        aws_secret_access_key: MYSECRET
        aws_region: MYREGION

    sources:
      - name: twitter-feed-c2
        module: twitter
        credentials: twitter-auth
        owner_screen_name: InQuest
        slug: c2-feed

      - name: twitter-search-opendir
        module: twitter
        credentials: twitter-auth
        q: '#opendir'

      - name: twitter-search-vt
        module: twitter
        credentials: twitter-auth
        q: virustotal.com

      - name: vendor-x
        module: rss
        url: http://example.com/rss.xml
        feed_type: messy

      - name: domain-masq-feed
        module: web
        url: http://example.com/feed.txt

    operators:
      - name: my-threatkb
        module: threatkb
        credentials: threatkb-auth
        allowed_sources: [twitter-feed-c2, vendor-x]
        state: Ingestor

      - name: my-crawler
        module: sqs
        credentials: aws-auth
        allowed_sources: [twitter-search-opendir, domain-masq-feed]
        artifact_types: [URL]
        queue_name: crawler
        domain: {domain}
        url: {url}
        source_type: url

      - name: my-analyzer
        module: sqs
        credentials: aws-auth
        allowed_sources: [twitter-search-vt]
        filter: https?://virustotal.com/.*/analysis
        artifact_types: [URL]
        queue_name: analyzer
        url: {url}
        source_type: virustotal

Note that in this example, our Crawler and Automated Analysis systems will be
watching the configured SQS queues for new artifacts. You can use SQS, or add
your own :ref:`custom operator plugins <custom-operator-plugins>` to send
artifacts wherever you want.

.. _full-circle-workflow:

Full-Circle
-----------

ThreatIngestor can both :ref:`read from <sqs-source>` and :ref:`write to
<sqs-operator>` SQS queues, which allows us to set up a "full circle" workflow.
(Note that you can also replace SQS with :ref:`Beanstalk <beanstalk-source>` or
:ref:`custom plugins <developing>` to
achieve the same effect.) In this workflow, we can extract artifacts from a
source, send them off to some SQS listener for processing, and that listener
can send the processed content back into ThreatIngestor's input queue for
extraction. Consider the following workflow:

.. image:: _static/mermaid-full-circle.png
   :align: center
   :alt: Flowchart with three inputs on the left, all feeding into
         ThreatIngestor in the center, which in turn feeds into two outputs
         on the right. The three inputs are "Twitter C2 List," "SQS Input
         Queue," and "Twitter Search: pastebin.com ioc." The outputs are
         "ThreatKB" and "SQS Pastebin Processor." The "SQS Pastebin Processor"
         output also flows into the "SQS Input Queue," completing the circular
         workflow.

Here, we have two Twitter sources: our C2 list and a search for "pastebin.com
ioc", and one SQS source: the input queue. We then have two operators:
ThreatKB, and an SQS Pastebin Processor application. We want all the C2s we
pull from the Twitter C2 list to go directly to ThreatKB. We also want any
pastebin links from either Twitter source to be sent to the SQS Pastebin
Processor. That Processor will grab the raw text from the pastebin link, and
send it to the ThreatIngestor input queue, where all the IOCs will be extracted
and sent to ThreatKB for further analysis. Here's an example config file that
accomplishes all that:

.. code-block:: yaml

    general:
        daemon: true
        sleep: 900
        state_path: state.db

    credentials:
      - name: twitter-auth
        token: MYTOKEN
        token_key: MYKEY
        con_secret_key: MYSECRETKEY
        con_secret: MYSECRET

      - name: threatkb-auth
        url: http://mythreatkb
        token: MYTOKEN
        secret_key: MYKEY

      - name: aws-auth
        aws_access_key_id: MYKEY
        aws_secret_access_key: MYSECRET
        aws_region: MYREGION

    sources:
      - name: twitter-feed-c2
        module: twitter
        credentials: twitter-auth
        owner_screen_name: InQuest
        slug: c2-feed

      - name: twitter-search-pastebin
        module: twitter
        credentials: twitter-auth
        q: pastebin.com ioc

      - name: sqs-input
        module: sqs
        credentials: aws-auth
        queue_name: threatingestor

    operators:
      - name: my-threatkb
        module: threatkb
        credentials: threatkb-auth
        allowed_sources: [sqs-input, twitter-feed-c2]
        state: Ingestor

      - name: pastebin-processor
        module: sqs
        credentials: aws-auth
        allowed_sources: [twitter-feed-c2, twitter-search-pastebin]
        artifact_types: [URL]
        filter: https?://pastebin.com/.+
        queue_name: pastebin-processor
        url: {url}

.. _queue-worker-workflow:

Queue Workers
-------------

The ThreatIngestor :ref:`plugin architecture <developing>` lets developers
integrate with external systems with relative ease - but not everything makes
sense as a plugin. Both source and operator plugins are expected to run to
completion quickly, then exit and wait for the next run before working again.
For long-running tasks (think VirusTotal / MultiAV scan, malware sandbox, web
crawler, domain brute force, etc), implementing them as plugins that block
until completion would break the workflow. Instead, consider using a queue
workflow.

In a typical queue workflow, an operator should queue up jobs for each artifact
it receives (typically with `SQS <sqs-operator>` or `Beanstalk
<beanstalk-operator>`), and an external tool we'll call a **queue worker**
should read from that queue and perform any necessary long-running tasks. When
the tasks are complete, the queue worker should send a job to another queue,
where it can be picked up by a ThreatIngestor queue source (like the `SQS
<sqs-source>` and `Beanstalk <beanstalk-source>` sources).

.. note::

    In the "Full-Circle" workflow above, the "SQS Pastebin Processor" is a queue
    worker.

Lets look at an example of a queue workflow using one of the provided queue
workers, the **File System Watcher**.

.. image:: _static/mermaid-queue-worker.png
   :align: center
   :alt: Flowchart with one input on the left (the File System Watcher),
         feeding into ThreatIngestor in the center, which in turn outputs
         into a MISP operator on the right.

Let's say we want to watch a directory for new YARA rules, and automatically
send them to our MISP server. Here's how the ThreatIngestor config would look:

.. code-block:: yaml

    general:
        daemon: true
        sleep: 900
        state_path: state.db

    credentials:
      - name: misp-auth
        url: http://mymisp
        key: MYKEY
        ssl: false

      - name: aws-auth
        aws_access_key_id: MYKEY
        aws_secret_access_key: MYSECRET
        aws_region: MYREGION

    sources:
      - name: fs-watcher
        module: sqs
        credentials: aws-auth
        queue_name: yara-rules
        paths: [content]
        reference: filename

    operators:
      - name: misp
        module: misp
        credentials: misp-auth
        artifact_types: [YARASignature]

In a separate file (we'll use ``fswatcher.yml``), set up the config for the
queue worker:

.. code-block:: yaml

    module: sqs
    aws_access_key_id: MYKEY
    aws_secret_access_key: MYSECRET
    aws_region: MYREGION
    queue_name: yara-rules
    watch_path: MY_RULES_FOLDER

Run the included File System Watcher::

    python3 -m threatingestor.extras.fswatcher fswatcher.yml

When new YARA rules are added to ``MY_RULES_FOLDER``, the File System Watcher
sends jobs to the ``yara-rules`` queue:

.. code-block:: json

    {
        "content": "rule myNewRule { condition: false }",
        "filename": "mynewrule.yara"
    }

Run ThreatIngestor, and it'll read from the ``yara-rules`` queue, extracting
artifacts from the ``content`` field in the job, and using the ``filename`` as
the artifact's reference text. When it finds YARA rules, it will send them off
through the MISP operator.

By combining custom plugins with custom queue workers, developers can extend
ThreatIngestor functionality to fit arbitrarily complex intel workflows.
