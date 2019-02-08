import unittest
from unittest.mock import Mock, patch
import json

import httpretty

import threatingestor.sources.sqs
import threatingestor.artifacts
import threatingestor.exceptions


class TestSQS(unittest.TestCase):

    @patch('boto3.resource')
    def setUp(self, boto3_resource):
        self.sqs = threatingestor.sources.sqs.Plugin('a', 'b', 'c', 'd', 'e', ['link'])

    def test_run_reads_messages_deletes_returns_artifacts(self):
        message = Mock()
        message.body = '{"link": "http://example.mock/path"}'
        self.sqs.queue.receive_messages.return_value = [message]

        saved_state, artifact_list = self.sqs.run(None)

        self.assertEqual(saved_state, None)
        self.sqs.queue.receive_messages.assert_called_once_with()
        message.delete.assert_called_once_with()
        self.assertIn('http://example.mock/path', [str(x) for x in artifact_list])
