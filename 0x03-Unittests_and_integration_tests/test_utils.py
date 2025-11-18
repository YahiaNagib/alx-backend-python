
#!/usr/bin/env python3

import utils
import unittest
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

        self.assertEqual(utils.access_nested_map(nested_map,path),expected_result)



    @parameterized.expand([
        [{"a": {"b": 2}, "b" : {"c":5 , "d":77}}, ("b", "t")],
        [{"a": {"b": 2}, "b" : {"c":5 , "d":77}}, ("b", "e")],
        [{"a": {"b": 2}}, ("z", "b")]
    ])
    def test_access_nested_map_exception(self,nested_map,path):

        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map,path)
     