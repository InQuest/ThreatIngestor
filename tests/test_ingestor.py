import unittest
from unittest.mock import Mock, patch

import threatingestor

class TestIngestor(unittest.TestCase):

    @patch('threatingestor.config.Config')
    def setUp(self, Config):
        mock_source_operator = Mock()
        mock_source_operator.return_value.run.return_value = (1,[])

        Config.return_value.sources.return_value = [
            ['test-twitter', mock_source_operator, {'q': 'test'}],
            ['test-rss', mock_source_operator, {'url': 'test'}],
        ]
        Config.return_value.operators.return_value = [
            ['test-threatkb', mock_source_operator, {'url': 'test'}],
            ['test-csv', mock_source_operator, {'filename': 'test'}],
        ]

        Config.return_value.state_path.return_value = ":memory:"
        self.app = threatingestor.Ingestor('test')
        self.app.statedb = Mock()

    @patch('threatingestor.config.Config')
    def test_init_creates_sources_operators_dicts(self, Config):
        attrs = {
            'sources.return_value': [
                ['test-twitter', Mock, {'q': 'test'}],
                ['test-rss', Mock, {'url': 'test'}],
            ],
            'operators.return_value': [
                ['test-threatkb', Mock, {'url': 'test'}],
                ['test-csv', Mock, {'filename': 'test'}],
            ],
        }
        Config.return_value.configure_mock(**attrs)

        Config.return_value.state_path.return_value = ":memory:"

        app = threatingestor.Ingestor('test')
        self.assertEqual(app.sources['test-twitter'].q, 'test')
        self.assertEqual(app.operators['test-csv'].filename, 'test')
        self.assertEqual(len(app.sources), 2)
        self.assertEqual(len(app.operators), 2)

    def test_run_checks_config_daemon(self):
        self.app.config.daemon.return_value = False
        self.app.run()
        self.app.config.daemon.assert_called_once()

    def test_run_once_calls_run_process_save_state(self):
        self.app.sources['test-twitter'].process.assert_not_called()
        self.app.sources['test-twitter'].run.assert_not_called()
        self.app.statedb.save_state.assert_not_called()

        self.app.run_once()
        self.app.sources['test-twitter'].process.assert_called()
        self.app.sources['test-twitter'].run.assert_called()
        self.app.statedb.save_state.assert_called()
        # should run 4 times, sources*operators.
        self.assertEqual(self.app.sources['test-twitter'].process.call_count, 4)
