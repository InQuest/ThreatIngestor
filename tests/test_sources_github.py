import unittest
from unittest.mock import patch
import datetime

import responses

import threatingestor.sources.github

API_RESPONSE_DATA = """
{
  "total_count": 40,
  "incomplete_results": false,
  "items": [
    {
      "id": 3081286,
      "name": "Tetris",
      "full_name": "dtrupenn/Tetris",
      "owner": {
        "login": "dtrupenn",
        "id": 872147,
        "avatar_url": "https://example.com/a.png",
        "gravatar_id": "",
        "url": "https://api.github.com/users/dtrupenn",
        "received_events_url": "https://api.github.com/users/dtrupenn/received_events",
        "type": "User"
      },
      "private": false,
      "html_url": "https://github.com/dtrupenn/Tetris",
      "description": "A C implementation of Tetris using Pennsim through LC4",
      "fork": false,
      "url": "https://api.github.com/repos/dtrupenn/Tetris",
      "created_at": "2012-01-01T00:31:50Z",
      "updated_at": "2013-01-05T17:58:47Z",
      "pushed_at": "2012-01-01T00:37:02Z",
      "homepage": "",
      "size": 524,
      "stargazers_count": 1,
      "watchers_count": 1,
      "language": "Assembly",
      "forks_count": 0,
      "open_issues_count": 0,
      "master_branch": "master",
      "default_branch": "master",
      "score": 10.309712
    }
  ]
}
"""


class TestGitHub(unittest.TestCase):

    def setUp(self):
        self.github = threatingestor.sources.github.Plugin('mygithub', 'CVE-2018-')

    @patch('threatingestor.sources.github.datetime')
    @responses.activate
    def test_run_returns_saved_state_tasks(self, mock_datetime):
        responses.add(responses.GET, threatingestor.sources.github.REPO_SEARCH_URL,
                body=API_RESPONSE_DATA)
        mock_datetime.datetime.utcnow.return_value = datetime.datetime(2018, 4, 30, 17, 5, 13, 194840)
        mock_datetime.datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        saved_state, artifact_list = self.github.run(None)
        self.assertIn('Manual Task: GitHub dtrupenn/Tetris', [str(x) for x in artifact_list])
        self.assertEqual(len(artifact_list), 1)
        self.assertEqual(saved_state, '2018-04-30T17:05:13Z')

    @responses.activate
    def test_requests_until_rel_is_not_next(self):
        responses.add(responses.GET,
                "https://api.github.com/search/repositories?q=Test",
                match_querystring=True, body=API_RESPONSE_DATA,
                headers={"Link":'<https://api.github.com/search/repositories?q=Test&page=2>; rel="next"'})
        responses.add(responses.GET,
                'https://api.github.com/search/repositories?q=Test&page=2',
                match_querystring=True, body=API_RESPONSE_DATA,
                headers={"Link":'<https://api.github.com/search/repositories?q=Test&page=3>; rel="next"'})
        responses.add(responses.GET,
                'https://api.github.com/search/repositories?q=Test&page=3',
                match_querystring=True, body=API_RESPONSE_DATA,
                headers={"Link":'<https://api.github.com/search/repositories?q=Test&page=3>; rel="last"'})

        params = {"q":"Test"}
        repo_list = self.github._repository_search(params)
        self.assertIn('Tetris', [str(x['name']) for x in repo_list])
        self.assertEqual(len(repo_list), 3)
