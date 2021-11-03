import os
import sys

cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)
from whun_helper.ranker import Ranker


def test_none_root():
    result = Ranker.level_rank_features(None, None)
    print("The result is " + result)
    assert result is None

