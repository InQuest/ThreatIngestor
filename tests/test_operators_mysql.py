import unittest
from unittest.mock import patch

import threatingestor.operators.mysql
import threatingestor.artifacts


class TestThreatSQLite(unittest.TestCase):

    @patch('pymysql.connect')
    def setUp(self, connect):
        self.mysql = threatingestor.operators.mysql.Plugin('a', 'b', 'c')

    @patch('pymysql.connect')
    def test_artifact_types_are_set_if_passed_in_else_default(self, connect):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        self.assertEqual(threatingestor.operators.mysql.Plugin('a', 'b', 'c', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEqual(threatingestor.operators.mysql.Plugin('a', 'b', 'c').artifact_types, [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
            threatingestor.artifacts.YARASignature,
            threatingestor.artifacts.Task
        ])

    @patch('pymysql.connect')
    def test_filter_string_and_allowed_sources_are_set_if_passed_in(self, connect):
        self.assertEqual(threatingestor.operators.mysql.Plugin('a', 'b', 'c', filter_string='test').filter_string, 'test')
        self.assertEqual(threatingestor.operators.mysql.Plugin('a', 'b', 'c', allowed_sources=['test-one']).allowed_sources, ['test-one'])
