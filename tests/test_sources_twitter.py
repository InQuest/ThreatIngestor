import unittest
from unittest.mock import patch

import threatingestor.sources.twitter


class TestTwitter(unittest.TestCase):

    @patch('twitter.Twitter')
    def setUp(self, Twitter):
        self.twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e')

    def teadDown(self):
        self.twitter.api.reset_mock()

    @patch('twitter.Twitter')
    def test_init_detects_search_type(self, Twitter):
        # default to @mentions
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e')
        self.assertEqual(twitter.endpoint._mock_name, 'mentions_timeline')
        self.assertEqual(twitter.name, 'a')

        # slug and owner_screen_name => list
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', slug='test', owner_screen_name='test')
        self.assertEqual(twitter.endpoint._mock_name, 'statuses')
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', slug='test')
        self.assertEqual(twitter.endpoint._mock_name, 'mentions_timeline')
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', owner_screen_name='test')
        self.assertEqual(twitter.endpoint._mock_name, 'mentions_timeline')

        # screen_name or user_id => user
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', screen_name='test')
        self.assertEqual(twitter.endpoint._mock_name, 'user_timeline')
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', user_id=1)
        self.assertEqual(twitter.endpoint._mock_name, 'user_timeline')

        # q => search
        twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', q='test')
        self.assertEqual(twitter.endpoint._mock_name, 'tweets')
        self.assertEqual(twitter.name, 'a')

    def test_run_respects_saved_state(self):
        self.twitter.run('12345')
        self.twitter.endpoint.assert_called_once_with(since_id='12345')

    def test_run_returns_newest_tweet_id_as_saved_state(self):
        self.twitter.endpoint.return_value = [
            {
                'text': 'test',
                'id_str': '12346',
                'user': {'screen_name': 'test'},
            },
            {
                'text': 'test',
                'id_str': '12345',
                'user': {'screen_name': 'test'},
            },
            {
                'text': 'test',
                'id_str': '12344',
                'user': {'screen_name': 'test'},
            },
        ]
        saved_state, artifact_list = self.twitter.run(None)
        self.assertEqual(saved_state, '12346')

    def test_run_supports_all_endpoints(self):
        # both supported return formats
        self.twitter.endpoint.return_value = [
            {
                'text': 'test',
                'id_str': '12345',
                'user': {'screen_name': 'test'},
            },
        ]
        saved_state, artifact_list = self.twitter.run(None)
        self.assertEqual(saved_state, '12345')

        self.twitter.endpoint.return_value = {
            'statuses': [
                {
                    'text': 'test',
                    'id_str': '12345',
                    'user': {'screen_name': 'test'},
                },
            ]
        }
        saved_state, artifact_list = self.twitter.run(None)
        self.assertEqual(saved_state, '12345')

    def test_run_returns_artifacts_correctly(self):
        self.twitter.endpoint.return_value = [
            {
                'text': 'hxxp://someurl.com/test',
                'id_str': '12345',
                'user': {'screen_name': 'test'},
            },
        ]
        saved_state, artifact_list = self.twitter.run(None)
        self.assertEqual(len(artifact_list), 3)
        self.assertIn('someurl.com', [str(x) for x in artifact_list])
        self.assertIn('http://someurl.com/test', [str(x) for x in artifact_list])
        self.assertEqual('https://twitter.com/test/status/12345', artifact_list[0].reference_link)

    def test_run_expands_tco_links_if_available(self):
        self.twitter.endpoint.return_value = [
            {
                'text': 'https://t.co/t3s7',
                'id_str': '12345',
                'user': {'screen_name': 'test'},
                'entities': {
                    'urls': [
                        {
                            'url': 'https://t.co/t3s7',
                            'expanded_url': 'hxxp://someurl.com/test',
                        },
                    ],
                },
            },
        ]
        # note: using hxxp above just to get the expanded url to be processed as
        # an obfuscated url and added to the threatingestor.artifacts list
        saved_state, artifact_list = self.twitter.run(None)
        self.assertEqual(len(artifact_list), 3)
        self.assertIn('someurl.com', [str(x) for x in artifact_list])
        self.assertIn('http://someurl.com/test', [str(x) for x in artifact_list])
        self.assertNotIn('t.co', [str(x) for x in artifact_list])
        self.assertNotIn('https://t.co/t3s7', [str(x) for x in artifact_list])

    @patch('twitter.Twitter')
    def test_run_includes_nonobfuscated_iff_configured(self, Twitter):
        # control
        self.twitter.endpoint.return_value = [
            {
                'text': 'http://someurl.com/test',
                'id_str': '12345',
                'user': {'screen_name': 'test'},
            },
        ]
        saved_state, artifact_list = self.twitter.run(None)
        self.assertEqual(len(artifact_list), 1)

        # test with defanged_only=False
        new_twitter = threatingestor.sources.twitter.Plugin('a', 'b', 'c', 'd', 'e', defanged_only=False)
        new_twitter.endpoint.return_value = [
            {
                'text': 'http://someurl.com/test',
                'id_str': '12345',
                'user': {'screen_name': 'test'},
            },
        ]
        saved_state, artifact_list = new_twitter.run(None)
        self.assertEqual(len(artifact_list), 3)

        self.assertIn('someurl.com', [str(x) for x in artifact_list])
        self.assertIn('http://someurl.com/test', [str(x) for x in artifact_list])
        self.assertEqual('https://twitter.com/test/status/12345', artifact_list[0].reference_link)
