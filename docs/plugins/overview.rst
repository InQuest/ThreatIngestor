Overview
========

ThreatIngestor can be easily extended to support other input and output
mechanisms through *Source* (input) and *Operator* (output) Python plugins. It
currently includes the following sources:

* Twitter
* RSS
* SQS
* Web
* Git
* GitHub Repository Search

And the following operators:

* ThreatKB
* CSV file
* Amazon SQS

The Twitter source can use three Twitter API endpoints out of the box: standard
search, user timeline, and Twitter lists. For examples of each, see
``config.ini.example``.

