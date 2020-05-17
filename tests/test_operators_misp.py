import unittest
from unittest.mock import patch, ANY as MOCK_ANY

import threatingestor.operators.misp
import threatingestor.artifacts


class TestThreatKB(unittest.TestCase):

    @patch('pymisp.ExpandedPyMISP')
    def setUp(self, ExpandedPyMISP):
        self.misp = threatingestor.operators.misp.Plugin('a', 'b')

    @patch('pymisp.ExpandedPyMISP')
    def test_tags_are_set_if_passed_in_else_default(self, ExpandedPyMISP):
        self.assertEqual(self.misp.tags, ['type:OSINT'])
        self.assertEqual(
            threatingestor.operators.misp.Plugin('a', 'b', tags=['c', 'd']).tags,
            ['c', 'd'],
        )

    def test_create_event_creates_event_and_objects(self):
        event = self.misp._create_event(
            threatingestor.artifacts.Domain(
                'test.com',
                'name',
                reference_link='link',
                reference_text='text',
            )
        )
        self.misp._update_or_create_event(event)
        self.misp.api.add_event.assert_called_once_with(event)

    def test_handle_domain_creates_domain(self):
        domain = threatingestor.artifacts.Domain('test.com', '', '')

        event = self.misp._create_event(domain)
        event = self.misp.handle_domain(domain, event)
        self.assertEqual(event.Attribute[0].value, str(domain))

    def test_handle_hash_creates_hash(self):
        hash = threatingestor.artifacts.Hash(
            '68b329da9893e34099c7d8ad5cb9c940', '', '')
        event = self.misp._create_event(hash)
        event = self.misp.handle_hash(hash, event)
        self.assertEqual(event.Attribute[0].value, str(hash))

        hash = threatingestor.artifacts.Hash(
            'adc83b19e793491b1c6ea0fd8b46cd9f32e592fc', '', '')
        event = self.misp._create_event(hash)
        event = self.misp.handle_hash(hash, event)
        self.assertEqual(event.Attribute[0].value, str(hash))

        hash = threatingestor.artifacts.Hash(
            '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b', '', '')
        event = self.misp._create_event(hash)
        event = self.misp.handle_hash(hash, event)
        self.assertEqual(event.Attribute[0].value, str(hash))

        hash = threatingestor.artifacts.Hash('invalid', '', '')
        event = self.misp._create_event(hash)
        event = self.misp.handle_hash(hash, event)
        self.assertEqual(event.Attribute, [])

    def test_handle_ipaddress_creates_ipaddress(self):
        ipaddress = threatingestor.artifacts.IPAddress('123.123.123.123', '', '')
        event = self.misp._create_event(ipaddress)
        event = self.misp.handle_ipaddress(ipaddress, event)
        self.assertEqual(event.Attribute[0].value, str(ipaddress))

    def test_handle_url_creates_url(self):
        url = threatingestor.artifacts.URL('http://example.com', '', '')
        event = self.misp._create_event(url)
        event = self.misp.handle_url(url, event)
        self.assertEqual(event.Attribute[0].value, str(url))

    def test_handle_yarasignature_creates_yarasignature(self):
        yara = threatingestor.artifacts.YARASignature('test', '', '')
        event = self.misp._create_event(yara)
        event = self.misp.handle_yarasignature(yara, event)
        self.assertEqual(event.Attribute[0].value, str(yara))

    def test_handle_artifact_creates_event(self):
        artifact = threatingestor.artifacts.URL('http://example.com', '', '')
        event = self.misp.handle_artifact(artifact)
        self.misp.api.add_event.assert_called_once()

    @patch('pymisp.ExpandedPyMISP')
    def test_artifact_types_are_set_if_passed_in_else_default(self, ExpandedPyMISP):
        artifact_types = [
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
        ]
        self.assertEqual(
            threatingestor.operators.misp.Plugin('a', 'b', artifact_types=artifact_types).artifact_types,
            artifact_types,
        )
        self.assertEqual(threatingestor.operators.misp.Plugin('a', 'b').artifact_types, [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
            threatingestor.artifacts.YARASignature
        ])

    @patch('pymisp.ExpandedPyMISP')
    def test_filter_string_and_allowed_sources_are_set_if_passed_in(self, ExpandedPyMISP):
        self.assertEqual(
            threatingestor.operators.misp.Plugin('a', 'b', filter_string='test').filter_string,
            'test',
        )
        self.assertEqual(
            threatingestor.operators.misp.Plugin('a', 'b', allowed_sources=['test-one']).allowed_sources,
            ['test-one'],
        )
