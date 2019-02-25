import unittest
from unittest.mock import Mock, patch
import json

import threatingestor.operators.beanstalk
import threatingestor.artifacts


class TestSQS(unittest.TestCase):

    @patch('greenstalk.Client')
    def setUp(self, boto3_client):
        self.beanstalk = threatingestor.operators.beanstalk.Plugin('a', 'b', 'c', test='{domain}')

    def test_put_sends_string(self):
        self.beanstalk.handle_artifact(threatingestor.artifacts.URL('http://example.com', 'a'))
        self.beanstalk.queue.put.assert_called_once_with('{"test": "example.com"}')
