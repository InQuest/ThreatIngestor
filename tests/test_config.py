import sys
import io
import unittest
from unittest.mock import mock_open, patch

import threatingestor.config
import threatingestor.artifacts
import threatingestor.sources.rss
import threatingestor.operators.csv
import threatingestor.operators.threatkb


class TestConfig(unittest.TestCase):

    def setUp(self):
        m = mock_open()
        with patch('threatingestor.config.io.open', m, create=True):
            self.config = threatingestor.config.Config('test')

    def test_daemon_returns_main_daemon_bool(self):
        # Mock true/false values for daemon variable.
        self.config.config = {
            'general': {
                'daemon': True,
            }
        }
        self.assertTrue(self.config.daemon())

        self.config.config = {
            'general': {
                'daemon': False,
            }
        }
        self.assertFalse(self.config.daemon())

    def test_state_path_returns(self):
        self.config.config = {
            'general': {
                'state_path': "/home/user/test",
            }
        }

        self.assertEqual(self.config.state_path(), "/home/user/test")

    def test_logging_returns_full_section(self):
        self.config.config = {
            'logging': {
                'arbitrary': 'test',
            }
        }

        self.assertEqual(self.config.logging(), {'arbitrary': 'test'})

    def test_notifiers_returns_full_section(self):
        self.config.config = {
            'notifiers': {
                'arbitrary': 'test',
            }
        }

        self.assertEqual(self.config.notifiers(), {'arbitrary': 'test'})

    def test_statsd_returns_full_section(self):
        self.config.config = {
            'statsd': {
                'arbitrary': 'test',
            }
        }

        self.assertEqual(self.config.statsd(), {'arbitrary': 'test'})

    def test_sleep_returns_main_sleep_int(self):
        self.config.config = {
            'general': {
                'sleep': 10,
            }
        }
        self.assertEqual(self.config.sleep(), 10)

        self.config.config = {
            'general': {
                'sleep': 90,
            }
        }
        self.assertEqual(self.config.sleep(), 90)

    def test_credentials_returns_dictionary_of_credentials(self):
        self.config.config = {
            'credentials': [
                {
                    'name': 'twitter-myuser',
                    'token': 'EXAMPLE',
                    'token_key': 'EXAMPLE',
                    'con_secret_key': 'EXAMPLE',
                    'con_secret': 'EXAMPLE'
                },
            ]
        }

        expected = {
            'name': 'twitter-myuser',
            'token': 'EXAMPLE',
            'token_key': 'EXAMPLE',
            'con_secret_key': 'EXAMPLE',
            'con_secret': 'EXAMPLE'
        }

        self.assertEqual(self.config.credentials('twitter-myuser') , expected)

    def test_sources_returns_list_of_all_source_tuples(self):
        self.config.config = {
            'sources': [
                {
                    'name': 'test-one',
                    'module': 'rss',
                    'url': 'example',
                },
                {
                    'name': 'test-two',
                    'module': 'rss',
                    'url': 'example',
                },
            ]
        }
        expected_sources = [
            ('test-one', threatingestor.sources.rss.Plugin, {'name': 'test-one', 'url': 'example'}),
            ('test-two', threatingestor.sources.rss.Plugin, {'name': 'test-two', 'url': 'example'}),
        ]
        self.assertEqual(self.config.sources(), expected_sources)

    def test_sources_list_includes_credentials(self):
        self.config.config = {
            'credentials': [
                {
                    'name': 'mycreds',
                    'token': 'mytoken',
                },
            ],
            'sources': [
                {
                    'name': 'test-one',
                    'module': 'rss',
                    'url': 'example',
                    'credentials': 'mycreds',
                },
                {
                    'name': 'test-two',
                    'module': 'rss',
                    'url': 'example',
                },
            ]
        }
        expected_sources = [
            ('test-one', threatingestor.sources.rss.Plugin,
                {'name': 'test-one', 'url': 'example', 'token': 'mytoken'}),
            ('test-two', threatingestor.sources.rss.Plugin, {'name': 'test-two', 'url': 'example'}),
        ]
        self.assertEqual(self.config.sources(), expected_sources)

    def test_sources_excludes_internal_options_from_kwargs(self):
        self.config.config = {
            'sources': [
                {
                    'name': 'test-one',
                    'module': 'rss',
                    'url': 'example',
                    'saved_state': 'test',
                },
            ]
        }

        expected_sources = [
            ('test-one', threatingestor.sources.rss.Plugin, {'url': 'example','name': 'test-one'}),
        ]
        self.assertEqual(self.config.sources(), expected_sources)

    def test_operators_returns_list_of_all_operator_tuples(self):
        self.config.config = {
            'operators': [
                {
                    'name': 'test-one',
                    'module': 'csv',
                    'filename': 'output.csv',
                },
                {
                    'name': 'test-three',
                    'module': 'csv',
                    'filename': 'output.csv',
                },
            ]
        }

        expected_operators = [
            ('test-one', threatingestor.operators.csv.Plugin, {'filename': 'output.csv'}),
            ('test-three', threatingestor.operators.csv.Plugin, {'filename': 'output.csv'}),
        ]
        self.assertEqual(self.config.operators(), expected_operators)

    def test_operators_list_includes_credentials(self):
        self.config.config = {
            'credentials': [
                {
                    'name': 'mycreds',
                    'token': 'mytoken',
                },
            ],
            'operators': [
                {
                    'name': 'test-one',
                    'module': 'csv',
                    'filename': 'output.csv',
                    'credentials': 'mycreds'
                },
                {
                    'name': 'test-three',
                    'module': 'csv',
                    'filename': 'output.csv',
                },
            ],
        }

        expected_operators = [
            ('test-one', threatingestor.operators.csv.Plugin, {'filename': 'output.csv', 'token': 'mytoken'}),
            ('test-three', threatingestor.operators.csv.Plugin, {'filename': 'output.csv'}),
        ]

        self.assertEqual(self.config.operators(), expected_operators)

    def test_operators_excludes_internal_options_from_kwargs(self):
        self.config.config = {
            'operators': [
                {
                    'name': 'test-one',
                    'module': 'csv',
                    'filename': 'output.csv',
                    'allowed_sources': ["mysource", "myothersource"],
                    'filter': '([^\.]google.com$|google.com[^/])',
                    'artifact_types': ["URL", "Domain"],
               },
            ]

        }

        expected_operators = [
            ('test-one', threatingestor.operators.csv.Plugin, {
                'filename': 'output.csv',
                'allowed_sources': ["mysource", "myothersource"],
                'filter_string': '([^\.]google.com$|google.com[^/])',
                'artifact_types': [
                    threatingestor.artifacts.URL,
                    threatingestor.artifacts.Domain,
                ],
            }),
        ]

        self.assertEqual(self.config.operators(), expected_operators)

    def test_load_plugin_returns_plugin_class(self):
        self.assertEqual(self.config._load_plugin(threatingestor.config.SOURCE, 'rss'),
                         threatingestor.sources.rss.Plugin)
        self.assertEqual(self.config._load_plugin(threatingestor.config.OPERATOR, 'csv'),
                         threatingestor.operators.csv.Plugin)

    @patch('importlib.import_module')
    def test_load_plugin_raises_pluginerror_if_no_plugin(self, import_module):
        # module doesn't exist
        import_module.side_effect = ImportError

        with self.assertRaises(threatingestor.exceptions.PluginError):
            self.config._load_plugin(threatingestor.config.OPERATOR, 'csv')

        # Plugin class doesn't exist
        import_module.side_effect = AttributeError

        with self.assertRaises(threatingestor.exceptions.PluginError):
            self.config._load_plugin(threatingestor.config.OPERATOR, 'csv')
