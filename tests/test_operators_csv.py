import unittest
try:
    from unittest.mock import patch, ANY as MOCK_ANY
except ImportError:
    from mock import patch, ANY as MOCK_ANY

import operators.csv
import artifacts


class TestCSV(unittest.TestCase):

    def setUp(self):
        self.csv = operators.csv.CSV('a')

    def test_artifact_types_are_set_if_passed_in_else_default(self):
        artifact_types = [artifacts.IPAddress, artifacts.URL]
        self.assertEquals(operators.csv.CSV('a', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEquals(operators.csv.CSV('a').artifact_types, [artifacts.Domain, artifacts.IPAddress, artifacts.URL])

    def test_filter_list_and_allowed_sources_are_set_if_passed_in(self):
        self.assertEquals(operators.csv.CSV('a', filter_string='test').filter_string, 'test')
        self.assertEquals(operators.csv.CSV('a', allowed_sources=['test-one']).allowed_sources, ['test-one'])
