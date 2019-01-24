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

.. code-block:: ini

    [main]
    daemon = true
    sleep = 900

    [source:twitter-feed-c2]
    module = twitter
    token = MYTOKEN
    token_key = MYKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    owner_screen_name = InQuest
    slug = c2-feed

    [source:twitter-search-opendir]
    module = twitter
    token = MYTOKEN
    token_key = MYKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    q = #opendir

    [source:twitter-search-vt]
    module = twitter
    token = MYTOKEN
    token_key = MYKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    q = virustotal.com

    [source:vendor-x]
    module = rss
    url = http://example.com/rss.xml
    feed_type = messy

    [source:domain-masq-feed]
    module = web
    url = http://example.com/feed.txt

    [operator:my-threatkb]
    module = threatkb
    allowed_sources = twitter-feed-c2, vendor-x
    url = http://mythreatkb
    token = MYTOKEN
    secret_key = MYKEY
    state = Ingestor

    [operator:my-crawler]
    module = sqs
    allowed_sources = twitter-search-opendir, domain-masq-feed
    artifact_types = URL
    aws_access_key_id = MYKEY
    aws_secret_access_key = MYSECRET
    aws_region = MYREGION
    queue_name = crawler
    domain = {domain}
    url = {url}
    source_type = url

    [operator:my-analyzer]
    module = sqs
    allowed_sources = twitter-search-vt
    filter = https?://virustotal.com/.*/analysis
    artifact_types = URL
    aws_access_key_id = MYKEY
    aws_secret_access_key = MYSECRET
    aws_region = MYREGION
    queue_name = analyzer
    url = {url}
    source_type = virustotal

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

.. code-block:: ini

    [main]
    daemon = true
    sleep = 900

    [source:twitter-feed-c2]
    module = twitter
    token = MYTOKEN
    token_key = MYKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    owner_screen_name = InQuest
    slug = c2-feed

    [source:twitter-search-pastebin]
    module = twitter
    token = MYTOKEN
    token_key = MYKEY
    con_secret_key = MYSECRETKEY
    con_secret = MYSECRET
    q = pastebin.com ioc

    [source:sqs-input]
    module = sqs
    aws_access_key_id = MYKEY
    aws_secret_access_key = MYSECRET
    aws_region = MYREGION
    queue_name = threatingestor

    [operator:my-threatkb]
    module = threatkb
    allowed_sources = sqs-input, twitter-feed-c2
    url = http://mythreatkb
    token = MYTOKEN
    secret_key = MYKEY
    state = Ingestor

    [operator:pastebin-processor]
    module = sqs
    allowed_sources = twitter-feed-c2, twitter-search-pastebin
    artifact_types = URL
    filter = https?://pastebin.com/.+
    aws_access_key_id = MYKEY
    aws_secret_access_key = MYSECRET
    aws_region = MYREGION
    queue_name = pastebin-processor
    url = {url}
