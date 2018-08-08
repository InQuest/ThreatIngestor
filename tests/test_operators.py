import unittest

import threatingestor.operators
import threatingestor.artifacts


class TestOperators(unittest.TestCase):

    def test_default_artifact_types_is_empty(self):
        self.assertEqual(threatingestor.operators.Operator().artifact_types, [])

    def test_handle_artifact_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            threatingestor.operators.Operator().handle_artifact(None)

    def test_process_includes_only_artifact_types(self):
        threatingestor.operators.Operator.handle_artifact = lambda x, y: x.artifacts.append(y)
        operator = threatingestor.operators.Operator()
        operator.artifact_types = [threatingestor.artifacts.Domain]
        operator.artifacts = []

        artifact_list = [
            threatingestor.artifacts.IPAddress('21.21.21.21', '', ''),
            threatingestor.artifacts.Domain('test.com', '', ''),
            threatingestor.artifacts.URL('http://example.com', '', ''),
            threatingestor.artifacts.Domain('example.com', '', ''),
        ]

        operator.process(artifact_list)
        self.assertTrue(all([isinstance(x, threatingestor.artifacts.Domain) for x in operator.artifacts]))
        self.assertEqual(len(operator.artifacts), 2)

        operator.artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        operator.artifacts = []
        operator.process(artifact_list)
        self.assertTrue(all([isinstance(x, threatingestor.artifacts.IPAddress) or isinstance(x, threatingestor.artifacts.URL) for x in operator.artifacts]))
        self.assertEqual(len(operator.artifacts), 2)

    def test_artifact_types_are_set_if_passed_in(self):
        artifact_types = [threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        self.assertEqual(threatingestor.operators.Operator(artifact_types=artifact_types).artifact_types, artifact_types)

    def test_process_includes_artifact_iff_filter_matches(self):
        threatingestor.operators.Operator.handle_artifact = lambda x, y: x.artifacts.append(y)
        operator = threatingestor.operators.Operator(filter_string='example.com')
        operator.artifact_types = [threatingestor.artifacts.Domain, threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        operator.artifacts = []

        artifact_list = [
            threatingestor.artifacts.IPAddress('21.21.21.21', '', ''),
            threatingestor.artifacts.Domain('test.com', '', ''),
            threatingestor.artifacts.URL('http://example.com', '', ''),
            threatingestor.artifacts.Domain('example.com', '', ''),
        ]

        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 2)
        self.assertNotIn(artifact_list[0], operator.artifacts)
        self.assertNotIn(artifact_list[1], operator.artifacts)
        self.assertIn(artifact_list[2], operator.artifacts)
        self.assertIn(artifact_list[3], operator.artifacts)

        operator.artifacts = []
        operator.filter_string = '21'
        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 1)
        self.assertIn(artifact_list[0], operator.artifacts)
        self.assertNotIn(artifact_list[1], operator.artifacts)
        self.assertNotIn(artifact_list[2], operator.artifacts)
        self.assertNotIn(artifact_list[3], operator.artifacts)

        operator.artifacts = []
        operator.filter_string = ''
        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 4)
        self.assertIn(artifact_list[0], operator.artifacts)
        self.assertIn(artifact_list[1], operator.artifacts)
        self.assertIn(artifact_list[2], operator.artifacts)
        self.assertIn(artifact_list[3], operator.artifacts)

        operator.artifacts = []
        operator.filter_string = 'is_domain'
        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 1)
        self.assertNotIn(artifact_list[0], operator.artifacts)
        self.assertNotIn(artifact_list[1], operator.artifacts)
        self.assertIn(artifact_list[2], operator.artifacts)
        self.assertNotIn(artifact_list[3], operator.artifacts)

    def test_process_includes_artifact_iff_source_name_is_allowed_or_allowed_is_empty(self):
        threatingestor.operators.Operator.handle_artifact = lambda x, y: x.artifacts.append(y)
        operator = threatingestor.operators.Operator()
        operator.artifact_types = [threatingestor.artifacts.Domain, threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        operator.artifacts = []

        artifact_list = [
            threatingestor.artifacts.IPAddress('21.21.21.21', 'source-1'),
            threatingestor.artifacts.Domain('test.com', 'source-1'),
            threatingestor.artifacts.URL('http://example.com', 'source-2'),
            threatingestor.artifacts.Domain('example.com', 'source-3'),
        ]

        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 4)
        self.assertIn(artifact_list[0], operator.artifacts)
        self.assertIn(artifact_list[1], operator.artifacts)
        self.assertIn(artifact_list[2], operator.artifacts)
        self.assertIn(artifact_list[3], operator.artifacts)

        operator.artifacts = []
        operator.allowed_sources = ['source-1']
        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 2)
        self.assertIn(artifact_list[0], operator.artifacts)
        self.assertIn(artifact_list[1], operator.artifacts)
        self.assertNotIn(artifact_list[2], operator.artifacts)
        self.assertNotIn(artifact_list[3], operator.artifacts)

        operator.artifacts = []
        operator.allowed_sources = ['source-2', 'source-3']
        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 2)
        self.assertNotIn(artifact_list[0], operator.artifacts)
        self.assertNotIn(artifact_list[1], operator.artifacts)
        self.assertIn(artifact_list[2], operator.artifacts)
        self.assertIn(artifact_list[3], operator.artifacts)

    def test_regex_allowed_sources(self):
        threatingestor.operators.Operator.handle_artifact = lambda x, y: x.artifacts.append(y)
        operator = threatingestor.operators.Operator(allowed_sources=['source-.*'])
        operator.artifact_types = [threatingestor.artifacts.Domain, threatingestor.artifacts.IPAddress, threatingestor.artifacts.URL]
        operator.artifacts = []

        artifact_list = [
            threatingestor.artifacts.IPAddress('21.21.21.21', 'source-1'),
            threatingestor.artifacts.Domain('test.com', 'source-1'),
            threatingestor.artifacts.URL('http://example.com', 'source-2'),
            threatingestor.artifacts.Domain('example.com', 'test-3'),
        ]

        operator.process(artifact_list)
        self.assertEqual(len(operator.artifacts), 3)
        self.assertIn(artifact_list[0], operator.artifacts)
        self.assertIn(artifact_list[1], operator.artifacts)
        self.assertIn(artifact_list[2], operator.artifacts)
        self.assertNotIn(artifact_list[3], operator.artifacts)
