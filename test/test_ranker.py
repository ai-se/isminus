import os
import sys

cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from src.whun.whun_helper.ranker import Ranker
from src.whun.whun_helper.method import Method


def test_none_root():
    result = Ranker.level_rank_features(None, None)
    print("The result is " + result)
    assert result is None


def test_none_root():
    result = Ranker.level_rank_features({}, {})
    print(result)
    assert result is None


def test_non_empty_items_rank():
    m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
    rank_result = Ranker.level_rank_features(m.tree, m.weights)
    assert (rank_result == m.rank).all