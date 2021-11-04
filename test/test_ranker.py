import os
import sys
from unittest import TestCase

cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from src.whun.whun_helper.ranker import Ranker
from src.whun.whun_helper.method import Method


def test_none_root_none_data():
    result = Ranker.level_rank_features(None, None)
    assert result is None


def test_none_root_empty_data():
    result = Ranker.level_rank_features({}, {})
    assert result is None


def test_non_empty_items_rank():
    m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
    rank_result = Ranker.level_rank_features(m.tree, m.weights)
    assert (rank_result == m.rank).all


def test_none_root_node_none_data():
    result = Ranker.rank_nodes(None, None)
    assert result is None


def test_none_root_node_empty_data():
    result = Ranker.rank_nodes({}, {})
    assert result is None


def test_non_empty_root_node():
    m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
    result = Ranker.level_rank_features(m.tree, m.rank)
    assert (result == m.cur_best_node).all


def test_none_pr_level_none_data():
    result = Ranker.pr_level(None)
    assert result is None


def test_none_pr_level_empty_data():
    result = Ranker.pr_level({})
    assert result is None


def test_non_empty_pr_level():
    m = Method(cur_dir + "/src/whun/XOMO/flight_bin.csv", cur_dir + "/src/whun/XOMO/flight_eval.csv", "")
    result = Ranker.pr_level(m.tree)
    t = TestCase()
    t.assertIsNotNone(result)
