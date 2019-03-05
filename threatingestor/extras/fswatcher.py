import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import boto3
import json

REGION_NAME = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
QUEUE_NAME = ''


class YARAHandler(PatternMatchingEventHandler):

    patterns = ["*.yar", "*.yara", "*.rule", "*.rules"]

    def sendYARA(self, rule_content):
        # connect to sqs

        sqs_client = boto3.client(
            'sqs',
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        queue_url = sqs_client.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
        content = json.dumps({'rule': rule_content})
        sqs_client.send_message(
            QueueUrl=queue_url,
            DelaySeconds=0,
            MessageBody=content
        )
        print("Sent successfully")

    def process(self, event):
        with open(event.src_path, 'r') as rule_source:
            rule_content = rule_source.read()
            self.sendYARA(rule_content)
            print("Rule: " + rule_content)
            self.retrieveYARA()

    def on_modified(self, event):
        print("Modified")
        self.process(event)

    def on_created(self, event):
        print("Created")
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(YARAHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
