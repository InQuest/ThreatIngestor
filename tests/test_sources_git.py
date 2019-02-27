import unittest
from unittest.mock import patch
import os

import httpretty

import threatingestor.sources.git


class TestGit(unittest.TestCase):

    def setUp(self):
        self.git = threatingestor.sources.git.Plugin('mygit', 'https://example.mock/user/repo.git', '/tmp/test/repo')

    @patch('subprocess.check_output')
    def test_internal_git_cmd_calls_subprocess_git(self, check_output):
        threatingestor.sources.git._git_cmd(['test'])
        check_output.assert_called_once_with(['git', 'test'])

    @patch('subprocess.check_output')
    @patch('os.chdir')
    def test_internal_git_cmd_chdir_manages_working_dir(self, chdir, check_output):
        current_dir = os.getcwd()
        threatingestor.sources.git._git_cmd_chdir('/test', ['test'])

        chdir.assert_any_call('/test')
        chdir.assert_called_with(current_dir)
        check_output.assert_called_once_with(['git', 'test'])

    @patch('threatingestor.sources.git._git_pull')
    @patch('threatingestor.sources.git._git_latest_hash')
    @patch('threatingestor.sources.git._git_diff_names')
    @patch('threatingestor.sources.git.io.open')
    def test_run_with_saved_state_pulls_diffs_parses(self, m_open, git_diff_names, git_latest_hash, git_pull):
        git_latest_hash.return_value = 'test_latest'
        git_diff_names.return_value = 'test_file\ntest_file.rule'
        m_open.return_value.__enter__.return_value.read.return_value = 'rule testrule { condition: false }'
        
        saved_state, artifact_list = self.git.run('test_saved')

        git_pull.assert_called_once_with(self.git.local_path)
        git_latest_hash.assert_called_once_with(self.git.local_path)
        git_diff_names.assert_called_once_with(self.git.local_path, 'test_saved')
        m_open.assert_called_once_with(os.path.join(self.git.local_path, 'test_file.rule'), 'r', encoding='utf-8', errors='ignore')
        self.assertEqual(saved_state, 'test_latest')
        self.assertIn('rule testrule { condition: false }', [str(x) for x in artifact_list])

    @patch('threatingestor.sources.git._git_clone')
    @patch('threatingestor.sources.git._git_latest_hash')
    @patch('threatingestor.sources.git._git_ls_files')
    @patch('threatingestor.sources.git.io.open')
    def test_run_without_saved_state_clones_lists_parses(self, m_open, git_ls_files, git_latest_hash, git_clone):
        git_latest_hash.return_value = 'test_latest'
        git_ls_files.return_value = 'test_file\ntest_file.yar'
        m_open.return_value.__enter__.return_value.read.return_value = 'rule testrule { condition: false }'
        
        saved_state, artifact_list = self.git.run(None)

        git_clone.assert_called_once_with(self.git.url, self.git.local_path)
        git_latest_hash.assert_called_once_with(self.git.local_path)
        git_ls_files.assert_called_once_with(self.git.local_path)
        m_open.assert_called_once_with(os.path.join(self.git.local_path, 'test_file.yar'), 'r', encoding='utf-8', errors='ignore')
        self.assertEqual(saved_state, 'test_latest')
        self.assertIn('rule testrule { condition: false }', [str(x) for x in artifact_list])

    @patch('threatingestor.sources.git._git_pull')
    @patch('threatingestor.sources.git._git_latest_hash')
    @patch('threatingestor.sources.git._git_diff_names')
    def test_run_with_saved_state_returns_early_if_nothing_new(self, git_diff_names, git_latest_hash, git_pull):
        git_latest_hash.return_value = 'test_saved'
        git_diff_names.return_value = ''
        
        saved_state, artifact_list = self.git.run('test_saved')

        git_pull.assert_called_once_with(self.git.local_path)
        git_latest_hash.assert_called_once_with(self.git.local_path)
        git_diff_names.assert_called_once_with(self.git.local_path, 'test_saved')
        self.assertEqual(saved_state, 'test_saved')
        self.assertEqual(len(artifact_list), 0)

