import os
import sys
cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from unittest import TestCase
from src.whun.whun_helper.method import Method


class TestMethod(TestCase):
    def test_no_file_error(self):
        self.assertRaises(FileNotFoundError, Method, "abc", "EVAL_FILE")