import unittest
from unittest.mock import Mock, patch
import json


import threatingestor.sources.abstract_json
import threatingestor.artifacts
import threatingestor.exceptions


class TestJSON(unittest.TestCase):

    def setUp(self):
        self.abs_json = threatingestor.sources.abstract_json.AbstractPlugin("name", [], "")

    def test_run(self):
        content_list = [{"testKey": "testValue"}]
        self.abs_json.get_objects = lambda x: (None, content_list)

        saved_state, artifact_list = self.abs_json.run(None)

        self.assertEqual(saved_state, None)

    def test_run_uses_reference_path_if_possible(self):
        content_list = [{"testContent": "http://example.com", "testRef": "myReference"}]
        abs_json = threatingestor.sources.abstract_json.AbstractPlugin("name", ["testContent"], "testRef")
        abs_json.get_objects = lambda x: (None, content_list)

        saved_state, artifact_list = abs_json.run(None)

        self.assertEqual(3, len(artifact_list))
        for artifact in artifact_list:
            self.assertEqual('myReference', artifact.reference_link)

    def test_run_uses_name_if_reference_path_not_found(self):
        content_list = [{"testContent": "http://example.com", "testRef": "myReference"}]
        abs_json = threatingestor.sources.abstract_json.AbstractPlugin("name", ["testContent"], "badRef")
        abs_json.get_objects = lambda x: (None, content_list)

        saved_state, artifact_list = abs_json.run(None)

        self.assertEqual(3, len(artifact_list))
        for artifact in artifact_list:
            self.assertEqual('name', artifact.reference_link)

    def test_run_extracts_artifacts(self):
        content_list = [{"testContent": "http://example.com", "testRef": "myReference"}]
        abs_json = threatingestor.sources.abstract_json.AbstractPlugin("name", ["testContent"], "testRef")
        abs_json.get_objects = lambda x: (None, content_list)

        saved_state, artifact_list = abs_json.run(None)

        self.assertEqual(3, len(artifact_list))
        self.assertIn('http://example.com', [str(x) for x in artifact_list])
