from TreeNode import TreeNode
from whun import split_bin


def sway(items, enough):
    if len(items) < enough:
        return TreeNode(items, None, None, None, True)
    west, east, west_items, east_items = split_bin(items, 10)
    east_node = sway(east_items, enough)
    west_node = sway(west_items, enough)
    root = TreeNode(east, west, east_node, west_node, False)
    root.east_id = east_node.id
    root.west_id = west_node.id
    return root
