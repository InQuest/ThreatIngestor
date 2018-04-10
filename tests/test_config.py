import unittest
try:
    from unittest.mock import mock_open, patch
except ImportError:
    from mock import mock_open, patch

import config
import sources.rss
import operators.csv


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
