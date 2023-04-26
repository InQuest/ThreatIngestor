# Comes with Python 3.6.9 installed by default
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install sqlite3
RUN apt-get install tesseract-ocr -y
RUN apt-get install python3-lxml -y

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python pytesseract numpy
RUN pip3 install threatingestor -U

COPY config.yml .