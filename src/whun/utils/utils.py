"""This module is related to utils"""
# pylint: disable=import-error,too-few-public-methods,
import os
import sys
from math import pi
import secrets
from whun_helper.tree_node import tree_node
cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(cur_dir)

def split_bin(items, total_group):
    """
    Function: sway
    Description: Takes a items of type Item and total groups,
    calcultes radius, take each item and put them in their radius
    and sort them by distance in reverse and converted all the items
    to the polar coordinate system and divide them into east and west.
    Inputs:
        -items:Item
        -total_group:integer
    Output:
        -west: representative of the group
        -east: representative of the group
        -west_items: all the others items except the representative
        -east_items: all the others items except the representative
    """
    west = []
    east = []
    west_items = []
    east_items = []
    rand = secrets.choice(items)
    max_r = -float('inf')
    min_r = float('inf')
    for item in items:
        item.r = sum(item.item)
        item.d = sum([a_i - b_i for a_i, b_i in zip(item.item, rand.item)])
        if item.r > max_r:
            max_r = item.r
        if item.r < min_r:
            min_r = item.r
    for item in items:
        item.r = (item.r - min_r) / (max_r - min_r + 10 ** (-32))
    R = {r.r for r in items}
    for k in R:
        group = [item for item in items if item.r == k]
        group.sort(key=lambda z: z.d, reverse=True)
        for i, value in enumerate(group):
            value.theta = (2 * pi * (i + 1)) / len(group)
    thk = max_r / total_group
    for g_value in range(total_group):
        group = [i for i in items if (g_value * thk) <= i.r <= ((g_value + 1) * thk)]
        group.sort(key=lambda x: x.theta)
        if len(group) > 0:
            east.append(group[0])
            west.append(group[len(group) - 1])
            for i in group:
                if i.theta <= pi:
                    east_items.append(i)
                else:
                    west_items.append(i)
    return west, east, west_items, east_items


def sway(items, enough):
    """
    Function: sway
    Description: Takes a specific number of items of type Item and returns
    the root after calculating the west,east,east_node and west_node
    Inputs:
        -items:Item
        -enough:integer
    Output:
        -root :TreeNode
    """
    if len(items) < enough:
        return tree_node(items, None, None, None, True)
    west, east, west_items, east_items = split_bin(items, 10)
    east_node = sway(east_items, enough)
    west_node = sway(west_items, enough)
    root = tree_node(east, west, east_node, west_node, False)
    root.east_id = east_node.id
    root.west_id = west_node.id
    return root
