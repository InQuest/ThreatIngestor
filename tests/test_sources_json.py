import unittest
from unittest.mock import Mock, patch
import json

import httpretty

import threatingestor.sources.abstract_json
import threatingestor.artifacts
import threatingestor.exceptions


class TestJSON(unittest.TestCase):

    def setUp(self):
        self.abs_json = threatingestor.sources.abstract_json.Plugin("name", [],"") 

    def test_run(self):
        
        content = json.loads('{"testKey": "testValue"}')
        self.abs_json.get_content = lambda x: content

        saved_state, artifact_list = self.abs_json.run(None)

        self.assertEqual(saved_state, None)
