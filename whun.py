import numpy as np
import pandas as pd
import scipy.stats as st
import pycosat
import secrets
import math
import random
import sys
from csv import reader
from itertools import count
from datetime import datetime
import time

# SETUP VARIABLES
folder = 'XOMO/'
filename = ''
eval_file = ''
NUM_FEATURES = 108
HUMAN_WEIGHT = 1.5

random.seed(datetime.now())


class IO:

    @staticmethod
    def read_dimacs(filename):
        file = open(filename)
        lines = file.readlines()
        names = []
        for line in lines[:NUM_FEATURES]:
            names.append(line.split(' ')[2][:-1])
        dimacs = lines[NUM_FEATURES+1:]
        cnf = [[int(s) for s in line.split(' ') if int(s) != 0]
               for line in dimacs]
        return names, cnf

    @staticmethod
    def get_question_text(filename, column):
        df = pd.read_csv(filename)
        return df[column].tolist()


class Item:
    max_features = -math.inf
    min_features = math.inf
    max_totalcost = -math.inf
    min_totalcost = math.inf
    max_known = -math.inf
    min_known = math.inf
    max_featuresused = -math.inf
    min_featuresused = math.inf
    costs = [secrets.randbelow(10) for _ in range(NUM_FEATURES)]
    defective = [bool(secrets.randbelow(2)) for _ in range(NUM_FEATURES)]
    used = [bool(secrets.randbelow(2)) for _ in range(NUM_FEATURES)]

    def __init__(self, item, eval):
        self.r = -1
        self.d = -1
        self.theta = -1
        self.item = item
        self.score = 0
        self.features = sum(item)
        self.selectedpoints = 0
        self.totalcost = sum(np.multiply(item, self.costs))
        self.knowndefects = sum(np.multiply(item, self.defective))
        self.featuresused = sum(np.multiply(item, self.used))
        self.risk = eval[0]
        self.effort = eval[1]
        self.defects = eval[2]
        self.months = eval[3]
        self.zitler_rank = eval[4]

    @staticmethod
    def calc_staticfeatures(items):
        for x in items:
            if x.features > Item.max_features:
                Item.max_features = x.features
            if x.features < Item.min_features:
                Item.min_features = x.features
            if x.totalcost > Item.max_totalcost:
                Item.max_totalcost = x.totalcost
            if x.totalcost < Item.min_totalcost:
                Item.min_totalcost = x.totalcost
            if x.knowndefects > Item.max_known:
                Item.max_known = x.knowndefects
            if x.knowndefects < Item.min_known:
                Item.min_known = x.knowndefects
            if x.featuresused > Item.max_featuresused:
                Item.max_featuresused = x.featuresused
            if x.featuresused < Item.min_featuresused:
                Item.min_featuresused = x.featuresused

    @staticmethod
    def rank_features(items, names):
        count = np.zeros(len(items[0].item))
        for item in items:
            count = np.add(count, item.item)
        rank = np.zeros(len(count))
        for i, v in enumerate(count):
            if v == 0:
                rank[i] = -1
                print("No", names[i])
            if v == (len(items)):
                rank[i] = -1
                print("All", names[i])
        return count, rank


class Oracle:
    def __init__(self, size):
        self.picked = [0] * size

    def pick(self, q_idx, node):
        west_points = 0
        east_points = 0
        # Check how many of these questions I have picked before
        for i in range(len(q_idx)):
            if node.east[0].item[q_idx[i]] and self.picked[q_idx[i]] == 1:
                east_points += 1
            elif node.west[0].item[q_idx[i]] and self.picked[q_idx[i]] == 1:
                west_points += 1
        # Random selection favoring the side i like the most
        if east_points + west_points > 0:
            weighted_selection = west_points / (east_points + west_points)
        else:
            weighted_selection = 0.5

        if random.random() < weighted_selection:
            selected = 0
        else:
            selected = 1
        # Update my vector of picked options
        if selected:
            for i in range(min(len(q_idx), 4)):
                if self.picked[q_idx[i]] == 0:
                    self.picked[q_idx[i]] = node.east[0].item[q_idx[i]]
        else:
            for i in range(min(len(q_idx), 4)):
                if self.picked[q_idx[i]] == 0:
                    self.picked[q_idx[i]] = node.west[0].item[q_idx[i]]
        # Return selected {0 = East, 1 = West}
        return selected


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
                tree_lvl.append((p[1], p[0].difference()))
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


class SATSolver:

    @staticmethod
    def get_solutions(cnf):
        global folder
        global eval_file
        evals = pd.read_csv(folder + eval_file).to_numpy()

        with open(cnf, 'r') as read_obj:
            binary_solutions = [[int(x) for x in rec]
                                for rec in reader(read_obj, delimiter=',')]
            items = []
            for i, item in enumerate(binary_solutions):
                items.append(Item(item, evals[i]))
            return items


class Search:

    @staticmethod
    def bfs(tree, target):
        # maintain a queue of paths
        queue = [[tree]]
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if target == node.score:
                    return path_id, node
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

    @staticmethod
    def bfsFinal(tree, target):
        # maintain a queue of paths
        queue = [[tree]]
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if target == node.weight and node.leaf:
                    return path_id, node
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

    @staticmethod
    def get_all_items(tree):
        # maintain a queue of paths
        queue = [[tree]]
        results = []
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if 1 == node.weight and node.leaf:
                    items = [x for x in node.east]
                    for item in items:
                        results.append(item)
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return results

    @staticmethod
    def get_all_leaves(tree):
        # maintain a queue of paths
        queue = [[tree]]
        results = []
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if node.leaf:
                    items = [x for x in node.east]
                    for item in items:
                        results.append(item)
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return results

    @staticmethod
    def get_item(tree, path):
        # maintain a queue of paths
        cur = tree
        for val in path[1:-1]:
            if cur.east_node.id == val:
                cur = cur.east_node
            elif cur.west_node.id == val:
                cur = cur.west_node
        last = path[-1]
        if cur.east_node.id == last:
            return cur.east[0].item
        elif cur.west_node.id == last:
            return cur.west[0].item


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


class Method:
    def __init__(self, filename):
        x = 5000
        sys.setrecursionlimit(x)
        self.items = SATSolver.get_solutions(filename)
        self.weights = [1] * len(self.items)
        self.tree = sway(self.items, 100)
        self.names = []
        self.rank = Ranker.level_rank_features(self.tree, self.weights)
        self.cur_best_node = Ranker.rank_nodes(self.tree, self.rank)
        # IO.get_question_text('terms_sentence_map.csv', 'sentence')
        self.questions = []

    def find_node(self):
        return Search.bfs(self.tree, self.cur_best_node)

    def pick_questions(self, node):
        diff = node.diff_array()
        ranked_ranks = sorted(self.rank, reverse=True)
        ranks = [x for x in ranked_ranks if x != 0]
        ranks.reverse()
        ranks = set(ranks)
        return self.get_index(diff, ranks)

    def adjust_tree(self, node, q_idx):
        if node.leaf:
            return
        if node.west:
            for i in q_idx:
                if i in node.west[0].item:
                    node.west_node.weight = 0
                    self.adjust_tree(node.west_node, q_idx)
        if node.east:
            for i in q_idx:
                if i in node.east[0].item:
                    node.east_node.weight = 0
                    self.adjust_tree(node.east_node, q_idx)

    def get_index(self, diff, ranks):
        questions = []
        for r in ranks:
            for i in range(len(diff)):
                if r == self.rank[i] and diff[i]:
                    questions.append(i)
        return questions

    def ask_questions(self, q_idx, node):
        east_options, west_options = [], []
        for i in range(len(q_idx)):
            if node.east[0].item[q_idx[i]]:
                east_options.append(self.questions[q_idx[i]])
            elif node.west[0].item[q_idx[i]]:
                west_options.append(self.questions[q_idx[i]])

        len_east = len(east_options)
        len_west = len(west_options)
        diff = abs(len_east - len_west)
        if len_east > len_west:
            for i in range(diff):
                west_options.append('           ')
        else:
            for i in range(diff):
                east_options.append('           ')
        print('Would you rather')
        print('Option 1 \t Option 2')
        for e, w in zip(east_options, west_options):
            print('1 -', e, '\t', '2 -', w)

    def adjust_weights(self, node, picked, q_idx):
        node.asked += 1
        east_options, west_options = [], []
        for i in range(len(q_idx)):
            if node.east[0].item[q_idx[i]]:
                east_options.append(q_idx[i])
            elif node.west[0].item[q_idx[i]]:
                west_options.append(q_idx[i])
        if picked == 0:  # EAST
            for i in range(len(q_idx)):
                self.weights[q_idx[i]] = 0
            self.adjust_down(node.west_node)
            self.adjust_tree(self.tree, west_options)
        if picked == 1:  # WEST
            for i in range(len(q_idx)):
                self.weights[q_idx[i]] = 0
            self.adjust_down(node.east_node)
            self.adjust_tree(self.tree, east_options)

    # OBSOLETE
    def adjust_up(self, node, depth=0, growth_factor=1.1):
        # check for presence of no answers. If so
        node.weight *= growth_factor
        growth_factor *= (0.9 ** depth)
        if node.east_node is not None and node.west_node is not None:
            self.adjust_up(node.east_node, depth + 1, growth_factor)
            self.adjust_up(node.west_node, depth + 1, growth_factor)

    def adjust_down(self, node, depth=0):
        # weight = 0
        node.weight = 0
        if node.east_node is not None and node.west_node is not None:
            self.adjust_down(node.east_node, depth + 1)
            self.adjust_down(node.west_node, depth + 1)

    def re_rank(self):
        self.rank = Ranker.level_rank_features(self.tree, self.weights)
        self.cur_best_node = Ranker.rank_nodes(self.tree, self.rank)

    def check_solution(self):
        if sum(self.rank) == 0:
            return Search.get_all_items(self.tree)
        value = Ranker.check_solution(self.tree)
        if value is None:
            return None
        if value == -1:
            return -1
        return Search.get_all_items(self.tree)

    def get_item(self, path):
        return Search.get_item(self.tree, path)

    def pick_best(self, solutions):
        sumsq = lambda *args: sum([i ** 2 for i in args])
        all_items = Search.get_all_leaves(self.tree)
        scores = list(
            map(lambda x: sumsq(x.risk, x.effort, x.defects, x.months, HUMAN_WEIGHT * (1 - (x.selectedpoints/100))), solutions))
        total_scores = list(map(lambda x: sumsq(x.risk, x.effort, x.defects,
                            x.months, HUMAN_WEIGHT * (1 - (x.selectedpoints/100))), all_items))
        minimizer = np.argmin(scores)
        solutions[minimizer].score = st.percentileofscore(
            total_scores, scores[minimizer])
        return solutions[minimizer]


def main():
    global filename
    global folder
    print(folder + filename)
    a, p, c, s, d, u, scores, t, x, e = [], [], [], [], [], [], [], [], [], []
    for i in range(100):
        print("--------------------RUN", i+1, '------------------------')
        start_time = time.time()
        m = Method(folder+filename)
        o = Oracle(len(m.rank))
        asked = 0
        first_qidx = set()
        while True:
            path, node = m.find_node()
            q_idx = m.pick_questions(node)
            for q in q_idx:
                first_qidx.add(q)
            asked += 1
            picked = o.pick(q_idx, node)
            m.adjust_weights(node, picked, q_idx)
            m.re_rank()
            solutions = m.check_solution()
            if solutions is not None:
                if solutions == -1:
                    print("No solutions were found matching your preferences.")
                    a.append(asked)
                    p.append(np.sum(o.picked))
                    c.append(-1)
                    s.append(-1)
                    d.append(-1)
                    u.append(-1)
                    x.append(-1)
                    e.append(-1)
                    scores.append(-1)
                    t.append(time.time() - start_time)
                    break
                for item in solutions:
                    item.selectedpoints = np.sum(np.multiply(
                        item.item, o.picked)) / np.sum(o.picked) * 100
                best = m.pick_best(solutions)
                print("Found a solution.")
                a.append(asked)
                p.append(np.sum(o.picked))
                c.append(best.effort)
                s.append(best.selectedpoints/100)
                d.append(best.risk)
                u.append(best.defects)
                x.append(best.months)
                e.append(best.zitler_rank/20000)
                scores.append(best.score)
                t.append(time.time() - start_time)
                break

    df = pd.DataFrame(
        {
            'Asked': a,
            'User Picked': p,
            'Effort': c,
            'Selected Points': s,
            'Risk': d,
            'Defects': u,
            'Months': x,
            'Score': scores,
            'Pure Score': e,
            'Time': t
        }).T
    df.to_csv('Scores/Score'+filename)
    return


if __name__ == "__main__":
    filenames = ['ground_bin.csv']
    eval_files = ['ground_eval.csv']
    for f, e in zip(filenames, eval_files):
        filename = f
        eval_file = e
        main()
