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
from utils import sway
from whun_helper.Item import Item
sys.path.append('/whun_helper')
from whun_helper.SATSolver import SATSolver
from whun_helper.Search import Search
from whun_helper.Ranker import Ranker
from whun_helper.Oracle import Oracle


# SETUP VARIABLES

# TODO: to be removed after all the refactor
folder = 'XOMO/'
filename = ''
eval_file = ''
NUM_FEATURES = 108
HUMAN_WEIGHT = 1.5

random.seed(datetime.now())


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
        self.items = SATSolver.get_solutions(filename, eval_file)
        self.weights = [1] * len(self.items)
        self.tree = sway.sway(self.items, 100)
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
            map(lambda x: sumsq(x.risk, x.effort, x.defects, x.months, HUMAN_WEIGHT * (1 - (x.selectedpoints / 100))),
                solutions))
        total_scores = list(map(lambda x: sumsq(x.risk, x.effort, x.defects,
                                                x.months, HUMAN_WEIGHT * (1 - (x.selectedpoints / 100))), all_items))
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
        print("--------------------RUN", i + 1, '------------------------')
        start_time = time.time()
        m = Method(folder + filename)
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
                s.append(best.selectedpoints / 100)
                d.append(best.risk)
                u.append(best.defects)
                x.append(best.months)
                e.append(best.zitler_rank / 20000)
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
    df.to_csv('Scores/Score' + filename)
    return


if __name__ == "__main__":
    filenames = ['flight_bin.csv']
    eval_files = ['flight_eval.csv']
    for f, e in zip(filenames, eval_files):
        filename = f
        eval_file = e
        main()
