import unittest
from unittest.mock import patch, Mock

import threatingestor.operators.twitter
import threatingestor.artifacts
import threatingestor.exceptions


class TestTwitter(unittest.TestCase):

    @patch('twitter.Twitter')
    def setUp(self, Twitter):
        self.twitter = threatingestor.operators.twitter.Plugin('a', 'b', 'c', 'd', 'status: {artifact}')

    def test_handle_artifact_interpolates_status_message(self):
        self.twitter._tweet = Mock()
        artifact = threatingestor.artifacts.URL('http://somedomain.com/test', 'test')
        expected_content = 'status: http://somedomain.com/test'
        self.twitter.handle_artifact(artifact)
        self.twitter._tweet.assert_called_once_with(expected_content, quote_tweet=None)

    def test_handle_artifact_passes_quote_tweet_for_tweet_links(self):
        self.twitter._tweet = Mock()
        artifact = threatingestor.artifacts.URL('http://somedomain.com/test', 'test',
                                                'https://twitter.com/InQuest/status/00000000000')
        expected_content = 'status: http://somedomain.com/test'
        self.twitter.handle_artifact(artifact)
        self.twitter._tweet.assert_called_once_with(expected_content,
                                                    quote_tweet='https://twitter.com/InQuest/status/00000000000')

        # make sure quote_tweet doesn't get set if the link isn't a tweet permalink
        self.twitter._tweet.reset_mock()
        artifact = threatingestor.artifacts.URL('http://somedomain.com/test', 'test',
                                                'https://twitter.com/help/')
        expected_content = 'status: http://somedomain.com/test'
        self.twitter.handle_artifact(artifact)
        self.twitter._tweet.assert_called_once_with(expected_content,
                                                    quote_tweet=None)

    def test_artifact_types_are_set_if_passed_in_else_default(self):
        artifact_types = [
            threatingestor.artifacts.URL,
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
        ]
        self.assertEqual(threatingestor.operators.twitter.Plugin('a', 'b', 'c', 'd', 'e',
                                                                  artifact_types=[threatingestor.artifacts.URL]).artifact_types,
                          [threatingestor.artifacts.URL])
        self.assertEqual(threatingestor.operators.twitter.Plugin('a', 'b', 'c', 'd', 'e').artifact_types,
                          artifact_types)

    def test_init_sets_config_args(self):
        operator = threatingestor.operators.twitter.Plugin('a', 'b', 'c', 'd', 'e',
                                                           filter_string='test',
                                                           allowed_sources=['test-one'])
        self.assertEqual(operator.filter_string, 'test')
        self.assertEqual(operator.allowed_sources, ['test-one'])

    def test_init_raises_if_bad_status(self):
        with self.assertRaises(threatingestor.exceptions.IngestorError):
            operator = threatingestor.operators.twitter.Plugin('a', 'b', 'c', 'd',
                                                               filter_string='test',
                                                               allowed_sources=['test-one'],
                                                               status=[])
