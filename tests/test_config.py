import sys
import io
import unittest
try:
    # py3
    from unittest.mock import mock_open, patch
    CONFIGPARSER = 'configparser.ConfigParser'
except ImportError:
    # py2
    from mock import mock_open, patch
    CONFIGPARSER = 'ConfigParser.ConfigParser'

import threatingestor.config
import threatingestor.artifacts
import threatingestor.sources.rss
import threatingestor.operators.csv
import threatingestor.operators.threatkb


class TestConfig(unittest.TestCase):

    @patch(CONFIGPARSER)
    def setUp(self, ConfigParser):
        self.config = threatingestor.config.Config('test')

    def test_daemon_returns_main_daemon_bool(self):
        self.config.config.getboolean.return_value = True
        self.assertTrue(self.config.daemon())
        self.config.config.getboolean.return_value = False
        self.assertFalse(self.config.daemon())

    def test_sleep_returns_main_sleep_int(self):
        self.config.config.getint.return_value = 10
        self.assertEqual(self.config.sleep(), 10)
        self.config.config.getint.return_value = 90
        self.assertEqual(self.config.sleep(), 90)

    def test_sources_returns_list_of_all_source_tuples(self):
        self.config.config.sections.return_value = [
            'source:test-one',
            'source:test-two',
            'not-a-source-or-operator',
            'operator:test-one',
            'operator:test-three',
        ]
        self.config.config.options.return_value = ['module']
        self.config.config.get.return_value = 'rss'
        expected_sources = [
            ('source:test-one', threatingestor.sources.rss.Plugin, {'name': 'test-one'}),
            ('source:test-two', threatingestor.sources.rss.Plugin, {'name': 'test-two'}),
        ]
        self.assertEqual(self.config.sources(), expected_sources)

    def test_sources_excludes_internal_options_from_kwargs(self):
        self.config.config.sections.return_value = [
            'source:test-one',
        ]
        self.config.config.options.return_value = ['module', 'saved_state', 'another_one']
        self.config.config.get.return_value = 'rss'
        expected_sources = [
            ('source:test-one', threatingestor.sources.rss.Plugin, {'another_one': 'rss', 'name': 'test-one'}),
        ]
        self.assertEqual(self.config.sources(), expected_sources)

    def test_operators_returns_list_of_all_operator_tuples(self):
        self.config.config.sections.return_value = [
            'source:test-one',
            'source:test-two',
            'not-a-source-or-operator',
            'operator:test-one',
            'operator:test-three',
        ]
        self.config.config.options.return_value = ['module']
        self.config.config.get.return_value = 'csv'
        expected_operators = [
            ('operator:test-one', threatingestor.operators.csv.Plugin, {}),
            ('operator:test-three', threatingestor.operators.csv.Plugin, {}),
        ]
        self.assertEqual(self.config.operators(), expected_operators)

    def test_operators_excludes_internal_options_from_kwargs(self):
        self.config.config.sections.return_value = [
            'operator:test-one',
        ]
        self.config.config.options.return_value = ['module', 'saved_state', 'another_one']
        self.config.config.get.return_value = 'csv'
        expected_operators = [
            ('operator:test-one', threatingestor.operators.csv.Plugin, {'another_one': 'csv'}),
        ]
        self.assertEqual(self.config.operators(), expected_operators)

    def test_save_state_writes_saved_state(self):
        self.config.config.set.assert_not_called()

        m = mock_open()
        with patch('threatingestor.config.open', m, create=True):
            m.assert_not_called()
            self.config.save_state('test', 'state')
            self.config.config.set.assert_called_once()
            m.assert_called_once()

    def test_get_state_reads_saved_state(self):
        self.config.config.get.return_value = 'test'
        self.config.config.read.assert_called_once()
        self.assertEqual(self.config.get_state(None), 'test')
        self.assertEqual(self.config.config.read.call_count, 2)

    def test_operators_include_artifact_list_in_kwargs(self):
        data = u'\n'.join([l.strip() for l in u"""
        [operator:test-one]
        module = threatkb
        artifact_types = URL,Domain, IPAddress , YARASignature
        another_one = test

        [operator:test-operator-two]
        module = csv
        artifact_types = IPAddress

        [operator:test-no-types]
        module = csv
        """.splitlines()])
        # can't use mock_open, since ConfigParser reacts poorly with it.
        # mock the correct global open depending on python version.
        open_func = '__builtin__.open'
        if sys.version_info[0] == 3:
            open_func = 'builtins.open'
        with patch(open_func, return_value=io.StringIO(data)):
            config_obj = threatingestor.config.Config('test')
            expected_operators = [
                ('operator:test-one', threatingestor.operators.threatkb.Plugin, {'another_one': 'test', 'artifact_types': [
                    threatingestor.artifacts.URL,
                    threatingestor.artifacts.Domain,
                    threatingestor.artifacts.IPAddress,
                    threatingestor.artifacts.YARASignature,
                ]}),
                ('operator:test-operator-two', threatingestor.operators.csv.Plugin, {'artifact_types': [threatingestor.artifacts.IPAddress]}),
                ('operator:test-no-types', threatingestor.operators.csv.Plugin, {}),
            ]
            self.assertEqual(config_obj.operators(), expected_operators)

    def test_operators_include_filter_in_kwargs(self):
        data = u'\n'.join([l.strip() for l in u"""
        [operator:test-one]
        module = threatkb
        artifact_types = URL,Domain, IPAddress , YARASignature
        filter = (some|regex.*)
        another_one = test

        [operator:test-operator-two]
        module = csv
        filter = is_domain, not is_ip

        [operator:test-no-filter]
        module = csv
        """.splitlines()])
        # can't use mock_open, since ConfigParser reacts poorly with it.
        # mock the correct global open depending on python version.
        open_func = '__builtin__.open'
        if sys.version_info[0] == 3:
            open_func = 'builtins.open'
        with patch(open_func, return_value=io.StringIO(data)):
            config_obj = threatingestor.config.Config('test')
            expected_operators = [
                ('operator:test-one', threatingestor.operators.threatkb.Plugin, {'another_one': 'test', 'filter_string': '(some|regex.*)', 'artifact_types': [
                    threatingestor.artifacts.URL,
                    threatingestor.artifacts.Domain,
                    threatingestor.artifacts.IPAddress,
                    threatingestor.artifacts.YARASignature,
                ]}),
                ('operator:test-operator-two', threatingestor.operators.csv.Plugin, {'filter_string': 'is_domain, not is_ip'}),
                ('operator:test-no-filter', threatingestor.operators.csv.Plugin, {}),
            ]
            self.assertEqual(config_obj.operators(), expected_operators)

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
