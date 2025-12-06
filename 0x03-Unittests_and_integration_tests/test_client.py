
#!/usr/bin/env python3

import unittest
import client, utils

from unittest.mock import Mock, patch
from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):

    Test_cases = [
            ["google", {"id": 1342004}],
            ["http://holberton.io", {"payload": False}]
    ]

    @patch('requests.get')
    def test_org(self,mock_get_json):

        success_mock = Mock()

        success_mock.json.return_value = {"id": 1342004}

        mock_get_json.return_value = success_mock

        response = client.GithubOrgClient('google')

        self.assertEqual(response.org['id'], 1342004)
