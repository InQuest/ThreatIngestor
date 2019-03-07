import io
import json
import yaml


import greenstalk
import boto3


import threatingestor.config
import threatingestor.exceptions


class QueueWorker:
    """Abstract base class for Queue Workers.

    Override do_work to implement child classes.
    """
    def __init__(self):
        self.config = {}
        self.queue = None


    def read_config(self, filename):
        """Read from a config YAML file and set up queues."""
        with io.open(filename, 'r') as f:
            self.config = yaml.safe_load(f.read())

        if self.config.get('module').lower() == 'sqs':
            self.queue = SQSInterface(
                self.config['aws_access_key_id'],
                self.config['aws_secret_access_key'],
                self.config['aws_region'],
                in_queue=self.config.get('in_queue'),
                out_queue=self.config.get('out_queue'))
        elif self.config.get('module').lower() == 'beanstalk':
            self.queue = BeanstalkInterface(
                self.config['host'],
                self.config['port'],
                in_queue=self.config.get('in_queue'),
                out_queue=self.config.get('out_queue'))
        else:
            raise threatingestor.exceptions.IngestorError('Invalid self.config.')


    def run_forever(self):
        """Do work forever.

        Note: There is no sleep here! If anything fails, it might spin out of
        control.
        """
        while True:
            content = self.do_work(self.queue.read_one())
            self.queue.write_one(content)


    def do_work(self, job):
        """Implement in child class.

        One or zero jobs are passed in from the queue.
        One or zero jobs are returned and sent to the queue.
        """
        raise NotImplementedError()


class SQSInterface:
    """A consistent Queue interface for SQS."""
    def __init__(self, aws_access_key_id, aws_secret_access_key,
                 aws_region, in_queue=None, out_queue=None):
        """Set up SQS connections.

        :param aws_access_key_id: AWS access key ID.
        :param aws_secret_access_key: AWS secret access key.
        :param aws_region: AWS region string.
        :param in_queue: Optional input queue name.
        :param out_queue: Optional output queue name.
        """
        self.in_queue = None
        self.out_queue = None

        if in_queue:
            resource = boto3.resource('sqs', region_name=aws_region,
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)
            self.in_queue = resource.get_queue_by_name(QueueName=in_queue)

        if out_queue:
            client = boto3.client('sqs', region_name=aws_region,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
            self.out_queue = client.get_queue_url(QueueName=out_queue)['QueueUrl']


    def read_one(self):
        """Read one or zero messages from the queue.

        :returns: Message body or None.
        """
        if not self.in_queue:
            return

        messages = self.in_queue.receive_messages(
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20)
        if not messages:
            return

        job = json.loads(messages[0].body)
        messages[0].delete()
        return job


    def write_one(self, content):
        """Write one message to the queue, if it exists."""
        if not self.out_queue or not content:
            return

        return self.out_queue.send_message(
            QueueUrl=self.out_queue,
            DelaySeconds=0,
            MessageBody=json.dumps(content)
        )


class BeanstalkInterface:
    """A consistent Queue interface for Beanstalk."""
    def __init__(self, host, port, in_queue=None, out_queue=None):
        """Set up Beanstalk connections.

        :param host: Beanstalk host.
        :param port: Beanstalk port.
        :param in_queue: Optional input queue name.
        :param out_queue: Optional output queue name.
        """
        self.in_queue = None
        self.out_queue = None

        if in_queue:
            self.in_queue = greenstalk.Client(host, port, watch=in_queue)

        if out_queue:
            self.out_queue = greenstalk.Client(host, port, use=out_queue)


    def read_one(self):
        """Read one or zero messages from the queue.

        :returns: Message body or None.
        """
        if not self.in_queue:
            return

        message = self.in_queue.reserve()
        job = json.loads(message.body)
        self.in_queue.delete(message)
        return job


    def write_one(self, content):
        """Write one message to the queue, if it exists."""
        if not self.out_queue or not content:
            return

        self.out_queue.put(json.dumps(content))
