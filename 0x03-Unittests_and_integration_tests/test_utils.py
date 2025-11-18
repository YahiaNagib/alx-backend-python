
#!/usr/bin/env python3

import utils
import unittest

class TestAccessNestedMap(unittest.TestCase):
    
    def test_access_nested_map(self):

        nested_map={"a": {"b": 2}, "b" : {"c":5 , "d":77}}
        path=("b", "d")

        self.assertEqual(utils.access_nested_map(nested_map,path),77)

        nested_map={"a": {"b": 2}}
        path=("a", "b")

        self.assertEqual(utils.access_nested_map(nested_map,path),2)