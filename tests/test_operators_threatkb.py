import unittest
try:
    from unittest.mock import patch, ANY as MOCK_ANY
except ImportError:
    from mock import patch, ANY as MOCK_ANY

import operators.threatkb
import artifacts


class TestThreatKB(unittest.TestCase):

    @patch('threatkb.ThreatKB')
    def setUp(self, ThreatKB):
        self.threatkb = operators.threatkb.ThreatKB('a', 'b', 'c', 'd')

    def test_handle_domain_creates_domain(self):
        self.threatkb.handle_artifact(artifacts.Domain('test.com', '', ''))
        self.threatkb.api.create.assert_called_once_with('c2dns', MOCK_ANY)

    def test_handle_ipaddress_creates_ipaddress(self):
        self.threatkb.handle_artifact(artifacts.IPAddress('123.123.123.123', '', ''))
        self.threatkb.api.create.assert_called_once_with('c2ips', MOCK_ANY)

    def test_handle_yarasignature_creates_yarasignature(self):
        self.threatkb.handle_artifact(artifacts.YARASignature('test', '', ''))
        self.threatkb.api.create.assert_called_once_with('import', MOCK_ANY)

    def test_artifact_types_are_set_if_passed_in_else_default(self):
        artifact_types = [artifacts.IPAddress, artifacts.URL]
        self.assertEquals(operators.threatkb.ThreatKB('a', 'b', 'c', 'd', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEquals(operators.threatkb.ThreatKB('a', 'b', 'c', 'd').artifact_types, [artifacts.Domain, artifacts.IPAddress,
                artifacts.YARASignature])

    def test_filter_string_and_allowed_sources_are_set_if_passed_in(self):
        self.assertEquals(operators.threatkb.ThreatKB('a', 'b', 'c', 'd', filter_string='test').filter_string, 'test')
        self.assertEquals(operators.threatkb.ThreatKB('a', 'b', 'c', 'd', allowed_sources=['test-one']).allowed_sources, ['test-one'])

    def test_handle_task_creates_task(self):
        self.threatkb.handle_artifact(artifacts.Task('', '', ''))
        self.threatkb.api.create.assert_called_once_with('tasks', MOCK_ANY)

