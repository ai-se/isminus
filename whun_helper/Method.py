"""This module is related to Method Class"""
# pylint: disable=import-error,invalid-name
import sys
import scipy.stats as st
import numpy as np
import configparams as cfg
from whun_helper.sat_solver import sat_solver
from whun_helper.search import search
from whun_helper.ranker import Ranker
from utils.utils import sway
sys.path.append('/whun_helper')

class Method((object)):
    def __init__(self, filename, eval_file):
        sys.setrecursionlimit(cfg.whunparams["RECURSION_LIMIT"])
        self.items = sat_solver.get_solutions(filename, eval_file)
        self.weights = [1] * len(self.items)
        self.tree = sway(self.items, 100)
        self.names = []
        self.rank = Ranker.level_rank_features(self.tree, self.weights)
        self.cur_best_node = Ranker.rank_nodes(self.tree, self.rank)
        # IO.get_question_text('terms_sentence_map.csv', 'sentence')
        self.questions = []

    def find_node(self):
        #"""A dummy docstring."""
        return search.bfs(self.tree, self.cur_best_node)

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
        for rank in ranks:
            for i, value in enumerate(diff):
                if rank == self.rank[i] and value:
                    questions.append(i)
        return questions

    def ask_questions(self, q_idx, node):
        east_options, west_options = [], []
        for _, value in enumerate(q_idx):
            if node.east[0].item[value]:
                east_options.append(self.questions[value])
            elif node.west[0].item[value]:
                west_options.append(self.questions[value])

        len_east = len(east_options)
        len_west = len(west_options)
        diff = abs(len_east - len_west)
        if len_east > len_west:
            for _ in range(diff):
                west_options.append('           ')
        else:
            for _ in range(diff):
                east_options.append('           ')
        print('Would you rather')
        print('Option 1 \t Option 2')
        for east_option, west_option in zip(east_options, west_options):
            print('1 -', east_option, '\t', '2 -', west_option)

    def adjust_weights(self, node, picked, q_idx):
        node.asked += 1
        east_options, west_options = [], []
        for _, value in enumerate(q_idx):
            if node.east[0].item[value]:
                east_options.append(value)
            elif node.west[0].item[value]:
                west_options.append(value)
        if picked == 0:  # EAST
            for _, value in enumerate(q_idx):
                self.weights[value] = 0
            self.adjust_down(node.west_node)
            self.adjust_tree(self.tree, west_options)
        if picked == 1:  # WEST
            for _, value in enumerate(q_idx):
                self.weights[value] = 0
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
            return search.get_all_items(self.tree)
        value = Ranker.check_solution(self.tree)
        if value is None:
            return None
        if value == -1:
            return -1
        return search.get_all_items(self.tree)

    def get_item(self, path):
        return search.get_item(self.tree, path)

    def pick_best(self, solutions):
        sumsq = lambda *args: sum([i ** 2 for i in args])
        all_items = search.get_all_leaves(self.tree)
        scores = list(
            map(lambda x: sumsq(x.risk, x.effort,
                                x.defects, x.months,
                                cfg.whunparams["HUMAN_WEIGHT"] * (1 - (x.selectedpoints / 100))),
                solutions))
        total_scores = list(
            map(lambda x: sumsq(x.risk, x.effort, x.defects,
                                x.months,
                                cfg.whunparams["HUMAN_WEIGHT"] * (1 - (x.selectedpoints / 100))),
                all_items))
        minimizer = np.argmin(scores)
        solutions[minimizer].score = st.percentileofscore(
            total_scores, scores[minimizer])
        return solutions[minimizer]
