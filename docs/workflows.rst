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
        state_path: state.sqlite3

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
(Note that you can also replace SQS with :ref:`custom plugins <developing>` to
achieve the same effect.) In this workflow, we can extract artifacts from a
source, send them off to some SQS listener for processing, and that listener
can send the processed content back into ThreatIngestor's input queue for
extraction. Consider the following workflow:

.. image:: _static/mermaid-full-circle.png
   :align: center

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
        state_path: state.sqlite3

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
