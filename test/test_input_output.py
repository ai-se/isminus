import os
import sys
from unittest import TestCase

cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from whun_helper.input_output import InputOutput


def test_get_question_text():
    list_expected = ['a', 'b', 'c', 'd']
    with open('test_resources/question.csv', 'r') as file:
        list_actual = InputOutput.get_question_text(file, 'question')
        print(list_actual)
        t = TestCase()
        t.assertCountEqual(list_actual, list_expected)
