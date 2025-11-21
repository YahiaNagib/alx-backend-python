
#!/usr/bin/env python3

import utils
import unittest

from unittest.mock import Mock, patch, call
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        [{"a": {"b": 2}, "b": {"c": 5, "d": 77}}, ("b", "d"), 77],
        [{"a": {"b": 2}, "b": {"c": 5, "d": 77}}, ("b", "c"), 5],
        [{"a": {"b": 2}}, ("a", "b"), 2]
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):

        # nested_map={"a": {"b": 2}, "b" : {"c":5 , "d":77}}
        # path=("b", "d")

        result = utils.access_nested_map(nested_map, path)

        self.assertEqual(result, expected_result)

    @parameterized.expand([
        [{"a": {"b": 2}, "b": {"c": 5, "d": 77}}, ("b", "t")],
        [{"a": {"b": 2}, "b": {"c": 5, "d": 77}}, ("b", "e")],
        [{"a": {"b": 2}}, ("z", "b")]
    ])
    def test_access_nested_map_exception(self, nested_map, path):

        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):

    Test_cases = [
            ["http://example.com", {"payload": True}],
            ["http://holberton.io", {"payload": False}]
        ]

    @parameterized.expand(Test_cases)
    @patch('utils.requests.get')
    def test_get_json(self, test_url, result, mock_get):

        success_mock = Mock(status_code=200, ok=True)
        success_mock.json.return_value = result

        mock_get.return_value = success_mock

        user_data = utils.get_json(test_url)
        self.assertEqual(user_data['payload'], result['payload'])

        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    This is a documentation for TestMemoize.
    This is a documentation for TestMemoize.
    This is a documentation for TestMemoize.
    """
    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        my_object = TestClass()

        # print(my_object.a_property)

        with patch.object(my_object, 'a_method') as mock_method:

            mock_method.return_value = 42

            result_1 = my_object.a_property
            result_2 = my_object.a_property

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)

            mock_method.assert_called_once()
