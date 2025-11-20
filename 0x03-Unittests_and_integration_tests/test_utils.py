
#!/usr/bin/env python3

import utils
import unittest

from unittest.mock import patch
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    
    @parameterized.expand([
        [{"a": {"b": 2}, "b" : {"c":5 , "d":77}}, ("b", "d"), 77],
        [{"a": {"b": 2}, "b" : {"c":5 , "d":77}}, ("b", "c"), 5],
        [{"a": {"b": 2}}, ("a", "b"), 2]
    ])
    def test_access_nested_map(self,nested_map,path,expected_result):

        # nested_map={"a": {"b": 2}, "b" : {"c":5 , "d":77}}
        # path=("b", "d")

        result = utils.access_nested_map(nested_map,path)

        self.assertEqual(result,expected_result)



    @parameterized.expand([
        [{"a": {"b": 2}, "b" : {"c":5 , "d":77}}, ("b", "t")],
        [{"a": {"b": 2}, "b" : {"c":5 , "d":77}}, ("b", "e")],
        [{"a": {"b": 2}}, ("z", "b")]
    ])
    def test_access_nested_map_exception(self,nested_map,path):

        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map,path)
     


class TestGetJson(unittest.TestCase):

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):

        test_url = "http://example.com"

        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
        "payload": True
    }


        user_data = utils.get_json(test_url)

        self.assertEqual(user_data['payload'],True)

        mock_get.assert_called_once_with(test_url)