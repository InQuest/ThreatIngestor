import unittest
from unittest.mock import patch, ANY as MOCK_ANY

import threatingestor.operators.misp
import threatingestor.artifacts


class TestThreatKB(unittest.TestCase):

    @patch('pymisp.PyMISP')
    def setUp(self, PyMISP):
        self.misp = threatingestor.operators.misp.Plugin('a', 'b')

    @patch('pymisp.PyMISP')
    def test_tags_are_set_if_passed_in_else_default(self, PyMISP):
        self.assertEqual(self.misp.tags, ['type:OSINT'])
        self.assertEqual(threatingestor.operators.misp.Plugin('a', 'b', tags=['c', 'd']).tags, ['c', 'd'])

    def test_create_event_creates_event_and_objects(self):
        event = self.misp._create_event(threatingestor.artifacts.Domain('test.com', 'name',
                                        reference_link='link', reference_text='text'))
        self.misp.api.new_event.assert_called_once_with(info=self.misp.event_info.format(source_name='name'))
        self.misp.api.add_tag.assert_called_once_with(event, self.misp.tags[0])
        self.misp.api.add_internal_link.assert_called_once_with(event, 'link')
        self.misp.api.add_internal_text.assert_called_once_with(event, 'text')
        self.misp.api.add_internal_other.assert_called_once_with(event, 'source:name')

    def test_handle_domain_creates_domain(self):
        self.misp.handle_artifact(threatingestor.artifacts.Domain('test.com', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_domain.assert_called_once_with(MOCK_ANY, 'test.com')

    def test_handle_hash_creates_hash(self):
        self.misp.handle_artifact(threatingestor.artifacts.Hash('68b329da9893e34099c7d8ad5cb9c940', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_hashes.assert_called_once_with(MOCK_ANY, md5='68b329da9893e34099c7d8ad5cb9c940')

        self.misp.api.reset_mock()
        self.misp.handle_artifact(threatingestor.artifacts.Hash('adc83b19e793491b1c6ea0fd8b46cd9f32e592fc', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_hashes.assert_called_once_with(MOCK_ANY, sha1='adc83b19e793491b1c6ea0fd8b46cd9f32e592fc')

        self.misp.api.reset_mock()
        self.misp.handle_artifact(threatingestor.artifacts.Hash('01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_hashes.assert_called_once_with(MOCK_ANY, sha256='01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b')

        self.misp.api.reset_mock()
        self.misp.handle_artifact(threatingestor.artifacts.Hash('invalid', '', ''))
        self.misp.api.new_event.assert_not_called()
        self.misp.api.add_hashes.assert_not_called()

    def test_handle_ipaddress_creates_ipaddress(self):
        self.misp.handle_artifact(threatingestor.artifacts.IPAddress('123.123.123.123', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_ipdst.assert_called_once_with(MOCK_ANY, '123.123.123.123')

    def test_handle_url_creates_url(self):
        self.misp.handle_artifact(threatingestor.artifacts.URL('http://example.com', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_url.assert_called_once_with(MOCK_ANY, 'http://example.com')

    def test_handle_yarasignature_creates_yarasignature(self):
        self.misp.handle_artifact(threatingestor.artifacts.YARASignature('test', '', ''))
        self.misp.api.new_event.assert_called_once()
        self.misp.api.add_yara.assert_called_once_with(MOCK_ANY, 'test')

    @patch('pymisp.PyMISP')
    def test_artifact_types_are_set_if_passed_in_else_default(self, PyMISP):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        self.assertEqual(threatingestor.operators.misp.Plugin('a', 'b', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEqual(threatingestor.operators.misp.Plugin('a', 'b').artifact_types, [
                threatingestor.artifacts.Domain,
                threatingestor.artifacts.Hash,
                threatingestor.artifacts.IPAddress,
                threatingestor.artifacts.URL,
                threatingestor.artifacts.YARASignature
        ])

    @patch('pymisp.PyMISP')
    def test_filter_string_and_allowed_sources_are_set_if_passed_in(self, PyMISP):
        self.assertEqual(threatingestor.operators.misp.Plugin('a', 'b', filter_string='test').filter_string, 'test')
        self.assertEqual(threatingestor.operators.misp.Plugin('a', 'b', allowed_sources=['test-one']).allowed_sources, ['test-one'])
