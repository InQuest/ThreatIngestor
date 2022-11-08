# Comes with Python 3.6.9 installed by default
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip3 install threatingestor
COPY config.yml .

# Run the ThreatIngestor without accessing /bin/bash container
CMD [ "threatingestor" , "config.yml"]