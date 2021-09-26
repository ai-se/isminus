import numpy as np


class Ranker:

    @staticmethod
    def level_rank_features(root, weights):
        if not root:
            return
        items_rank = np.zeros(len(root.west[0].item))
        q = [[root, 1]]
        while len(q):
            p = q[0]
            q.pop(0)
            if p[0].west is not None and p[0].east is not None:
                diff = p[0].diff_array()
                for i, d in enumerate(diff):
                    if d and items_rank[i] == 0:
                        items_rank[i] = p[1] * weights[i]
            if p[0].west_node:
                q.append([p[0].west_node, p[1] + 1])
            if p[0].east_node:
                q.append([p[0].east_node, p[1] + 1])
        print(int(np.sum([1 for x in items_rank if x > 0])),
              "Total number of important questions")
        return items_rank

    @staticmethod
    def rank_nodes(root, rank):
        if not root:
            return
        largest = -100000000
        q = [[root, 1]]
        while len(q):
            p = q[0]
            q.pop(0)
            if p[0].west is not None and p[0].east is not None:
                diff = p[0].diff_array()
                res = np.multiply(diff, rank)
                p[0].score = (np.sum(res) * p[0].weight) / np.sum(diff)
                if p[0].score > largest:
                    largest = p[0].score
            if p[0].west_node:
                q.append([p[0].west_node, p[1] + 1])
            if p[0].east_node:
                q.append([p[0].east_node, p[1] + 1])
        return largest

    @staticmethod
    def pr_level(root):
        tree_lvl = []
        if not root:
            return
        q = [[root, 1]]
        while len(q):
            p = q[0]
            q.pop(0)
            if p[0].west is not None and p[0].east is not None:
                tree_lvl.append((p[1], p[0].TreeNode.difference()))
            if p[0].west_node:
                q.append([p[0].west_node, p[1] + 1])
            if p[0].east_node:
                q.append([p[0].east_node, p[1] + 1])
        return tree_lvl

    @staticmethod
    def check_solution(root):
        count = 0
        if not root:
            return
        q = [[root, 1]]
        while len(q):
            p = q[0]
            q.pop(0)
            if p[0].weight == 1 and p[0].leaf:
                count += 1
            if p[0].west_node:
                q.append([p[0].west_node, p[1] + 1])
            if p[0].east_node:
                q.append([p[0].east_node, p[1] + 1])
        print("Count =", count)
        if count == 1:
            return 1
        if count < 1:
            return -1
        return None
