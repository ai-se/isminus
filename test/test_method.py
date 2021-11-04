import os
import sys
cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from unittest import TestCase
from src.whun.whun_helper.method import Method


class TestMethod(TestCase):
    def test_no_file_error(self):
        self.assertRaises(FileNotFoundError, Method, "abc", "EVAL_FILE")

    def test_method_init(self):
        method = Method(cur_dir+'/test/test_resources/method_bin.csv', cur_dir+'/test/test_resources/method_eval.csv')
        t = TestCase()
        t.assertEqual(len(method.rank), 108)
        t.assertEqual(len(method.weights), 200)
        t.assertEqual(len(method.items), 200)


    #def test_find_node_empty(self):
    #    method = Method(cur_dir+'/test/test_resources/method_bin.csv', cur_dir+'/test/test_resources/method_eval.csv')
    #    method.tree = None
    #   t = TestCase()
    #    result = method.find_node()
    #    t.assertEqual(result, None)

    def test_find_node(self):
        method = Method(cur_dir+'/test/test_resources/method_bin.csv', cur_dir+'/test/test_resources/method_eval.csv')
        t = TestCase()
        print(method.tree)
        path, node = method.find_node()
        t.assertIsNotNone(path)
        t.assertIsNotNone(node)
