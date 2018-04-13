import unittest

import operators
import artifacts


class TestOperators(unittest.TestCase):

    def test_default_artifact_types_is_empty(self):
        self.assertEquals(operators.Operator().artifact_types, [])

    def test_handle_artifact_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            operators.Operator().handle_artifact(None)

    def test_process_includes_only_artifact_types(self):
        operators.Operator.handle_artifact = lambda x, y: x.artifacts.append(y)
        operator = operators.Operator()
        operator.artifact_types = [artifacts.Domain]
        operator.artifacts = []

        artifact_list = [
            artifacts.IPAddress('21.21.21.21', '', ''),
            artifacts.Domain('test.com', '', ''),
            artifacts.URL('http://example.com', '', ''),
            artifacts.Domain('example.com', '', ''),
        ]

        operator.process(artifact_list)
        self.assertTrue(all([isinstance(x, artifacts.Domain) for x in operator.artifacts]))
        self.assertEquals(len(operator.artifacts), 2)

        operator.artifact_types = [artifacts.IPAddress, artifacts.URL]
        operator.artifacts = []
        operator.process(artifact_list)
        self.assertTrue(all([isinstance(x, artifacts.IPAddress) or isinstance(x, artifacts.URL) for x in operator.artifacts]))
        self.assertEquals(len(operator.artifacts), 2)

    def test_artifact_types_are_set_if_passed_in(self):
        artifact_types = [artifacts.IPAddress, artifacts.URL]
        self.assertEquals(operators.Operator(artifact_types=artifact_types).artifact_types, artifact_types)
