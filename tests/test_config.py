import sys
import io
import unittest
try:
    from unittest.mock import mock_open, patch
except ImportError:
    from mock import mock_open, patch

import config
import artifacts
import sources.rss
import operators.csv
import operators.threatkb


class TestConfig(unittest.TestCase):

    @patch('ConfigParser.ConfigParser')
    @patch('configparser.ConfigParser')
    def setUp(self, ConfigParser2, ConfigParser3):
        self.config = config.Config('test')

    def test_daemon_returns_main_daemon_bool(self):
        self.config.config.getboolean.return_value = True
        self.assertTrue(self.config.daemon())
        self.config.config.getboolean.return_value = False
        self.assertFalse(self.config.daemon())

    def test_sleep_returns_main_sleep_int(self):
        self.config.config.getint.return_value = 10
        self.assertEquals(self.config.sleep(), 10)
        self.config.config.getint.return_value = 90
        self.assertEquals(self.config.sleep(), 90)

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
            ('source:test-one', sources.rss.RSS, {}),
            ('source:test-two', sources.rss.RSS, {}),
        ]
        self.assertEquals(self.config.sources(), expected_sources)

    def test_sources_excludes_internal_options_from_kwargs(self):
        self.config.config.sections.return_value = [
            'source:test-one',
        ]
        self.config.config.options.return_value = ['module', 'saved_state', 'another_one']
        self.config.config.get.return_value = 'rss'
        expected_sources = [
            ('source:test-one', sources.rss.RSS, {'another_one': 'rss'}),
        ]
        self.assertEquals(self.config.sources(), expected_sources)

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
            ('operator:test-one', operators.csv.CSV, {}),
            ('operator:test-three', operators.csv.CSV, {}),
        ]
        self.assertEquals(self.config.operators(), expected_operators)

    def test_operators_excludes_internal_options_from_kwargs(self):
        self.config.config.sections.return_value = [
            'operator:test-one',
        ]
        self.config.config.options.return_value = ['module', 'saved_state', 'another_one']
        self.config.config.get.return_value = 'csv'
        expected_operators = [
            ('operator:test-one', operators.csv.CSV, {'another_one': 'csv'}),
        ]
        self.assertEquals(self.config.operators(), expected_operators)

    def test_save_state_writes_saved_state(self):
        self.config.config.set.assert_not_called()

        m = mock_open()
        with patch('config.open', m, create=True):
            m.assert_not_called()
            self.config.save_state('test', 'state')
            self.config.config.set.assert_called_once()
            m.assert_called_once()

    def test_get_state_reads_saved_state(self):
        self.config.config.get.return_value = 'test'
        self.config.config.read.assert_called_once()
        self.assertEquals(self.config.get_state(None), 'test')
        self.assertEquals(self.config.config.read.call_count, 2)

    def test_operators_include_artifact_list_in_kwargs(self):
        data = '\n'.join([l.strip() for l in """
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
        with patch(open_func, return_value=io.BytesIO(data)):
            config_obj = config.Config('test')
            expected_operators = [
                ('operator:test-one', operators.threatkb.ThreatKB, {'another_one': 'test', 'artifact_types': [
                    artifacts.URL,
                    artifacts.Domain,
                    artifacts.IPAddress,
                    artifacts.YARASignature,
                ]}),
                ('operator:test-operator-two', operators.csv.CSV, {'artifact_types': [artifacts.IPAddress]}),
                ('operator:test-no-types', operators.csv.CSV, {}),
            ]
            self.assertEquals(config_obj.operators(), expected_operators)

    def test_operators_include_filter_in_kwargs(self):
        data = '\n'.join([l.strip() for l in """
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
        with patch(open_func, return_value=io.BytesIO(data)):
            config_obj = config.Config('test')
            expected_operators = [
                ('operator:test-one', operators.threatkb.ThreatKB, {'another_one': 'test', 'filter_string': '(some|regex.*)', 'artifact_types': [
                    artifacts.URL,
                    artifacts.Domain,
                    artifacts.IPAddress,
                    artifacts.YARASignature,
                ]}),
                ('operator:test-operator-two', operators.csv.CSV, {'filter_string': 'is_domain, not is_ip'}),
                ('operator:test-no-filter', operators.csv.CSV, {}),
            ]
            self.assertEquals(config_obj.operators(), expected_operators)
