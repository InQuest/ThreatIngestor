import unittest
from unittest.mock import Mock, patch

import threatingestor.sources.beanstalk


class TestBeanstalk(unittest.TestCase):

    @patch('greenstalk.Client')
    def setUp(self, greenstalk_client):
        self.beanstalk = threatingestor.sources.beanstalk.Plugin('a', 'b', 'c', 'd', ['content'])

    def test_run_reads_messages_deletes_returns_artifacts(self):
        message = Mock()
        message.body = '{"content": "http://example.mock/path"}'
        self.beanstalk.queue.reserve.return_value = message

        saved_state, artifact_list = self.beanstalk.run(None)

        self.assertEqual(saved_state, None)
        self.beanstalk.queue.reserve.assert_called_with(timeout=1)
        self.beanstalk.queue.delete.assert_called()
        self.assertIn('http://example.mock/path', [str(x) for x in artifact_list])
