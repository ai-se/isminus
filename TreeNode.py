from itertools import count

import numpy as np


class TreeNode:
    _ids = count(0)

    def __init__(self, east, west, east_node, west_node, leaf):
        self.id = next(self._ids)
        self.east = east
        self.west = west
        self.east_id = -1
        self.west_id = -1
        self.east_node = east_node
        self.west_node = west_node
        self.score = 0
        self.weight = 1
        self.asked = 0
        self.leaf = leaf

    def difference(self):
        w = np.array(self.west[0].item)
        e = np.array(self.east[0].item)
        res = np.logical_xor(w, e)
        return np.sum(res)

    def diff_array(self):
        w = np.array(self.west[0].item)
        e = np.array(self.east[0].item)
        res = np.logical_xor(w, e)
        return res
