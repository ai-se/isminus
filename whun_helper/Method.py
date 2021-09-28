import scipy.stats as st
import sys
import numpy as np
sys.path.append('/whun_helper')
from csv import reader
from whun_helper.Item import Item
from utils.utils import sway, split_bin
from whun_helper.rankerhelper import Ranker
from whun_helper.Search import Search
from whun_helper.SATSolver import SATSolver
import pandas as pd
import configparams as cfg

class Method:
    def __init__(self, filename, eval_file):
        x = 5000
        sys.setrecursionlimit(x)
        self.items = SATSolver.get_solutions(filename, eval_file)
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
            map(lambda x: sumsq(x.risk, x.effort, x.defects, x.months, cfg.whunparams["HUMAN_WEIGHT"] * (1 - (x.selectedpoints / 100))),
                solutions))
        total_scores = list(map(lambda x: sumsq(x.risk, x.effort, x.defects,
                                                x.months, cfg.whunparams["HUMAN_WEIGHT"] * (1 - (x.selectedpoints / 100))), all_items))
        minimizer = np.argmin(scores)
        solutions[minimizer].score = st.percentileofscore(
            total_scores, scores[minimizer])
        return solutions[minimizer]

