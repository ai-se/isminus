import os
import sys
import numpy as np
cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from unittest import TestCase
from src.whun.whun_helper.oracle import Oracle
from src.whun.whun_helper.method import Method


def test_non_empty_init():
    m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
    o = Oracle(len(m.rank))
    assert len(o.picked) == len(m.rank)


def test_pick():
    for i in range(5):
        m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
        o = Oracle(len(m.rank))
        asked = 0
        first_qidx = set()
        t = TestCase()
        while True:
            _, node = m.find_node()
            q_idx = m.pick_questions(node)
            for q in q_idx:
                first_qidx.add(q)
            asked += 1
            picked = o.pick(q_idx, node)
            t.assertIn(picked, [0, 1])
            m.adjust_weights(node, picked, q_idx)
            m.re_rank()
            solutions = m.check_solution()
            if solutions is not None:
                if solutions == -1:
                    break
                for item in solutions:
                    item.selectedpoints = np.sum(np.multiply(
                        item.item, o.picked)) / np.sum(o.picked) * 100
                break
