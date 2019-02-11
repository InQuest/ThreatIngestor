import unittest
from unittest.mock import Mock, patch
import json

import threatingestor.operators.sqs
import threatingestor.artifacts


class TestSQS(unittest.TestCase):

    @patch('boto3.client')
    def setUp(self, boto3_client):
        self.sqs = threatingestor.operators.sqs.Plugin('a', 'b', 'c', 'd')

    def test_process_discards_ip_urls_if_filtered_out(self):
        # control
        self.sqs._put = Mock()
        self.sqs.filter_string = 'is_domain'
        self.sqs.handle_artifact(threatingestor.artifacts.URL('http://somedomain.com/test', '', ''))
        self.sqs._put.assert_called_once()

        # test
        self.sqs._put.reset_mock()
        self.sqs.process([threatingestor.artifacts.URL('http://123.123.123.123/test', '', '')])
        self.sqs._put.assert_not_called()

    def test_handle_artifact_passes_kwargs_url(self):
        self.sqs._put = Mock()
        self.sqs.kwargs = {
            'test_arg': 'test_val',
            'test_domain': '{domain}',
            'test_url': '{url}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_domain': 'somedomain.com',
            'test_url': 'http://somedomain.com/test',
        }
        self.sqs.handle_artifact(threatingestor.artifacts.URL('http://somedomain.com/test', '', ''))
        self.sqs._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_hash(self):
        self.sqs._put = Mock()
        self.sqs.kwargs = {
            'test_arg': 'test_val',
            'test_hash': '{hash}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_hash': 'test',
        }
        self.sqs.handle_artifact(threatingestor.artifacts.Hash('test', '', ''))
        self.sqs._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_ipaddress(self):
        self.sqs._put = Mock()
        self.sqs.kwargs = {
            'test_arg': 'test_val',
            'test_ipaddress': '{ipaddress}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_ipaddress': 'test',
        }
        self.sqs.handle_artifact(threatingestor.artifacts.IPAddress('test', '', ''))
        self.sqs._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_domain(self):
        self.sqs._put = Mock()
        self.sqs.kwargs = {
            'test_arg': 'test_val',
            'test_domain': '{domain}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_domain': 'test',
        }
        self.sqs.handle_artifact(threatingestor.artifacts.Domain('test', '', ''))
        self.sqs._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_yarasignature(self):
        self.sqs._put = Mock()
        self.sqs.kwargs = {
            'test_arg': 'test_val',
            'test_yarasignature': '{yarasignature}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_yarasignature': 'test',
        }
        self.sqs.handle_artifact(threatingestor.artifacts.YARASignature('test', '', ''))

        self.sqs._put.assert_called_once_with(expected_content)

    @patch('boto3.client')
    def test_artifact_types_are_set_if_passed_in_else_default(self, boto3_client):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        self.assertEqual(threatingestor.operators.sqs.Plugin('a', 'b', 'c', 'd', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEqual(threatingestor.operators.sqs.Plugin('a', 'b', 'c', 'd').artifact_types, [threatingestor.artifacts.URL])

    @patch('boto3.client')
    def test_init_sets_config_args(self, boto3_client):
        operator = threatingestor.operators.sqs.Plugin('a', 'b', 'c', 'd', filter_string='test', allowed_sources=['test-one'])
        self.assertEqual(operator.filter_string, 'test')
        self.assertEqual(operator.allowed_sources, ['test-one'])
