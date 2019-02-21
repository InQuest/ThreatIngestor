import unittest

import threatingestor.operators.sqlite
import threatingestor.artifacts


class TestThreatSQLite(unittest.TestCase):

    def setUp(self):
        # Set up an in-memory SQL database, we're doing full integration tests here.
        self.sqlite = threatingestor.operators.sqlite.Plugin(':memory:')

    def test_create_tables_creates_tables_for_each_artifact_type(self):
        # Since _create_tables was called by the constructor, just assert that
        # all the expected tables exist and have a sane structure.
        self.sqlite.cursor.execute('SELECT count() FROM sqlite_master WHERE type="table"')
        table_count = self.sqlite.cursor.fetchone()
        self.assertEqual((len(self.sqlite.artifact_types),), table_count)

        for artifact_type in self.sqlite.artifact_types:
            type_name = artifact_type.__name__.lower()
            self.sqlite.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" and name=?', (type_name,))
            table_name = self.sqlite.cursor.fetchone()
            self.assertEqual((type_name,), table_name)

        # Sanity test.
        self.sqlite.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" and name="domain"')
        table_name = self.sqlite.cursor.fetchone()
        self.assertEqual(("domain",), table_name)

    def test_handle_artifact_inserts_or_ignores(self):
        # First insert.
        self.sqlite.handle_artifact(threatingestor.artifacts.Domain(
            'test.com', 'name', reference_link='link', reference_text='text'
        ))
        query = 'SELECT artifact, reference_link, reference_text FROM domain WHERE artifact="test.com"'
        self.sqlite.cursor.execute(query)
        data = self.sqlite.cursor.fetchone()
        self.assertEqual(('test.com', 'link', 'text'), data)

        # Subsequent inserts are ignored.
        self.sqlite.handle_artifact(threatingestor.artifacts.Domain(
            'test.com', 'name', reference_link='different link', reference_text='more text'
        ))
        query = 'SELECT count() FROM domain WHERE artifact="test.com"'
        self.sqlite.cursor.execute(query)
        count = self.sqlite.cursor.fetchone()
        self.assertEqual((1,), count)

        query = 'SELECT artifact, reference_link, reference_text FROM domain WHERE artifact="test.com"'
        self.sqlite.cursor.execute(query)
        data = self.sqlite.cursor.fetchone()
        self.assertEqual(('test.com', 'link', 'text'), data)

    def test_artifact_types_are_set_if_passed_in_else_default(self):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        self.assertEqual(threatingestor.operators.sqlite.Plugin(':memory:', artifact_types=artifact_types).artifact_types, artifact_types)
        self.assertEqual(threatingestor.operators.sqlite.Plugin(':memory:').artifact_types, [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
            threatingestor.artifacts.YARASignature,
            threatingestor.artifacts.Task
        ])

    def test_filter_string_and_allowed_sources_are_set_if_passed_in(self):
        self.assertEqual(threatingestor.operators.sqlite.Plugin(':memory:', filter_string='test').filter_string, 'test')
        self.assertEqual(threatingestor.operators.sqlite.Plugin(':memory:', allowed_sources=['test-one']).allowed_sources, ['test-one'])
