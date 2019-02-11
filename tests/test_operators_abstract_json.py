import unittest
from unittest.mock import Mock, patch
import json

import threatingestor.operators.abstract_json
import threatingestor.artifacts


class TestAbstractJSON(unittest.TestCase):

    def setUp(self):
        self.abstract_json = threatingestor.operators.abstract_json.AbstractPlugin()

    def test_process_discards_ip_urls_if_filtered_out(self):
        # control
        self.abstract_json._put = Mock()
        self.abstract_json.filter_string = 'is_domain'
        self.abstract_json.handle_artifact(threatingestor.artifacts.URL('http://somedomain.com/test', '', ''))
        self.abstract_json._put.assert_called_once()

        # test
        self.abstract_json._put.reset_mock()
        self.abstract_json.process([threatingestor.artifacts.URL('http://123.123.123.123/test', '', '')])
        self.abstract_json._put.assert_not_called()

    def test_handle_artifact_passes_kwargs_url(self):
        self.abstract_json._put = Mock()
        self.abstract_json.kwargs = {
            'test_arg': 'test_val',
            'test_domain': '{domain}',
            'test_url': '{url}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_domain': 'somedomain.com',
            'test_url': 'http://somedomain.com/test',
        }
        self.abstract_json.handle_artifact(threatingestor.artifacts.URL('http://somedomain.com/test', '', ''))
        self.abstract_json._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_hash(self):
        self.abstract_json._put = Mock()
        self.abstract_json.kwargs = {
            'test_arg': 'test_val',
            'test_hash': '{hash}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_hash': 'test',
        }
        self.abstract_json.handle_artifact(threatingestor.artifacts.Hash('test', '', ''))
        self.abstract_json._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_ipaddress(self):
        self.abstract_json._put = Mock()
        self.abstract_json.kwargs = {
            'test_arg': 'test_val',
            'test_ipaddress': '{ipaddress}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_ipaddress': 'test',
        }
        self.abstract_json.handle_artifact(threatingestor.artifacts.IPAddress('test', '', ''))
        self.abstract_json._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_domain(self):
        self.abstract_json._put = Mock()
        self.abstract_json.kwargs = {
            'test_arg': 'test_val',
            'test_domain': '{domain}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_domain': 'test',
        }
        self.abstract_json.handle_artifact(threatingestor.artifacts.Domain('test', '', ''))
        self.abstract_json._put.assert_called_once_with(expected_content)

    def test_handle_artifact_passes_kwargs_yarasignature(self):
        self.abstract_json._put = Mock()
        self.abstract_json.kwargs = {
            'test_arg': 'test_val',
            'test_yarasignature': '{yarasignature}',
        }
        expected_content = {
            'test_arg': 'test_val',
            'test_yarasignature': 'test',
        }
        self.abstract_json.handle_artifact(threatingestor.artifacts.YARASignature('test', '', ''))

        self.abstract_json._put.assert_called_once_with(expected_content)

    def test_artifact_types_are_set_if_passed_in_else_default(self):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]

        self.assertEqual(threatingestor.operators.abstract_json.AbstractPlugin( artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEqual(threatingestor.operators.abstract_json.AbstractPlugin().artifact_types, [threatingestor.artifacts.URL])
        
    def test_init_sets_config_args(self):
        operator = threatingestor.operators.abstract_json.AbstractPlugin( filter_string='test', allowed_sources=['test-one'])
        self.assertEqual(operator.filter_string, 'test')
        self.assertEqual(operator.allowed_sources, ['test-one'])
