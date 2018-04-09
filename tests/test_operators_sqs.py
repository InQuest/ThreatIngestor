import unittest
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
import json

import operators.sqs
import artifacts


class TestSQS(unittest.TestCase):

    @patch('boto3.client')
    def setUp(self, boto3_client):
        self.sqs = operators.sqs.SQS('a', 'b', 'c', 'd')

    def test_handle_url_discards_ip_urls(self):
        # control
        self.sqs._sqs_put = Mock()
        self.sqs.handle_url(artifacts.URL('http://somedomain.com/test', '', ''))
        self.sqs._sqs_put.assert_called_once()

        # test
        self.sqs._sqs_put.reset_mock()
        self.sqs.handle_url(artifacts.URL('http://123.123.123.123/test', '', ''))
        self.sqs._sqs_put.assert_not_called()

    def test_handle_url_passes_kwargs(self):
        self.sqs._sqs_put = Mock()
        self.sqs.kwargs = {
            'test_arg': 'test_val',
            'test_domain': '{domain}',
            'test_url': '{url}',
        }
        expected_content = json.dumps({
            'test_arg': 'test_val',
            'test_domain': 'somedomain.com',
            'test_url': 'http://somedomain.com/test',
        })
        self.sqs.handle_url(artifacts.URL('http://somedomain.com/test', '', ''))
        self.sqs._sqs_put.assert_called_once_with(expected_content)
