import unittest
from unittest.mock import patch, ANY as MOCK_ANY

import threatingestor.operators.csv
import threatingestor.artifacts


class TestCSV(unittest.TestCase):

    def setUp(self):
        self.csv = threatingestor.operators.csv.Plugin('a')

    def test_artifact_types_are_set_if_passed_in_else_default(self):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        self.assertEqual(threatingestor.operators.csv.Plugin('a', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEqual(threatingestor.operators.csv.Plugin('a').artifact_types, [threatingestor.artifacts.Domain, threatingestor.artifacts.Hash, threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL])

    def test_filter_list_and_allowed_sources_are_set_if_passed_in(self):
        self.assertEqual(threatingestor.operators.csv.Plugin('a', filter_string='test').filter_string, 'test')
        self.assertEqual(threatingestor.operators.csv.Plugin('a', allowed_sources=['test-one']).allowed_sources, ['test-one'])
