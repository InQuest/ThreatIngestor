# Comes with Python 3.6.9 installed by default
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install sqlite3

RUN pip3 install threatingestor \
                 twitter \
                 feedparser

COPY config.yml .