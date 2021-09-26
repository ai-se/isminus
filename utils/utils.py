import math
import secrets
from TreeNode import TreeNode
#from whun import split_bin

def split_bin(items, total_group):
    west = []
    east = []
    west_items = []
    east_items = []
    rand = secrets.choice(items)
    max_r = -math.inf
    min_r = math.inf
    for x in items:
        x.r = sum(x.item)
        x.d = sum([a_i - b_i for a_i, b_i in zip(x.item, rand.item)])
        if x.r > max_r:
            max_r = x.r
        if x.r < min_r:
            min_r = x.r
    for x in items:
        x.r = (x.r - min_r) / (max_r - min_r + 10 ** (-32))
    R = set([r.r for r in items])
    for k in R:
        g = [item for item in items if item.r == k]
        g.sort(key=lambda z: z.d, reverse=True)
        for i in range(len(g)):
            g[i].theta = (2 * math.pi * (i + 1)) / len(g)
    thk = max_r / total_group
    for a in range(total_group):
        g = [i for i in items if (a * thk) <= i.r <= ((a + 1) * thk)]
        g.sort(key=lambda x: x.theta)
        if len(g) > 0:
            east.append(g[0])
            west.append(g[len(g) - 1])
            for i in g:
                if i.theta <= math.pi:
                    east_items.append(i)
                else:
                    west_items.append(i)
    return west, east, west_items, east_items


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
