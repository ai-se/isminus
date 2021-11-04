import os
import sys
cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from unittest import TestCase
from src.whun.whun_helper.oracle import Oracle
from src.whun.whun_helper.method import Method


def test_non_empty_init():
    m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
    o = Oracle(len(m.rank))
    assert len(o.picked) == len(m.rank)