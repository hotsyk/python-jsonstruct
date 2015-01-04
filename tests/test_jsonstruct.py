#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_jsonstruct
----------------------------------

Tests for `python-jsonstruct` module.
"""
import json
import unittest

from jsonstruct import jsonstruct


class TestJsonstruct(unittest.TestCase):

    def setUp(self):
        self.struct = jsonstruct.Struct

    def test_creatingobject(self):
        data = {'test': 1, 'test2': 2}
        struct = self.struct(**data)
        self.assertEqual(struct.test, 1)
        self.assertEqual(struct.test2, 2)
        self.assertEqual(struct.test3, None)
        with self.assertRaises(AttributeError):
            struct._mytest
            struct.__mytest

    def test_getdata(self):
        data = {'test': 1, 'test2': 2}
        struct = self.struct(**data)
        returned_data = struct.get_data()
        self.assertEqual(returned_data, data)

    def test_getjson(self):
        data = {'test': 1, 'test2': 2}
        struct = self.struct(**data)
        jsondata = json.dumps(data)
        returned_json = struct.get_json()
        self.assertEqual(returned_json, jsondata)

    def test_recursivedata(self):
        data = {'test': 1, 'test2': {'level2_key': 1}}
        struct = self.struct(**data)
        self.assertEqual(struct.test, 1)
        self.assertEqual(struct.test2.level2_key, 1)
        with self.assertRaises(AttributeError):
            struct.test2._mytest
            struct.test2.__mytest
        returned_data = struct.get_data()
        self.assertEqual(returned_data, data)

    def test_create_data_tuple(self):
        data = {'test': 1, 'test2': ({'t1': 1}, 2)}
        struct = self.struct(**data)
        self.assertEqual(struct.test, 1)
        self.assertEqual(struct.test2[0].t1, 1)
        self.assertEqual(struct.test2[1], 2)

    def test_create_data_list(self):
        data = {'test': 1, 'test2': [{'t1': 1}, 2]}
        struct = self.struct(**data)
        self.assertEqual(struct.test, 1)
        self.assertEqual(struct.test2[0].t1, 1)
        self.assertEqual(struct.test2[1], 2)


if __name__ == '__main__':
    unittest.main()
