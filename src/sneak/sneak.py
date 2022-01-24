"""This module is related to WHUN implementation"""
import os
import random
import sys
import time
from datetime import datetime
import numpy as np
import pandas as pd
import math
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)
from config import configparams as cfg
from sneak_helper.method import Method
from sneak_helper.oracle import Oracle
from sneak_helper.ui_helper import UIHelper
from src.sneak.utils.utils import semi_supervised_optimizer
from PyQt5.QtWidgets import *

random.seed(datetime.now())
ui_obj = None
picked_array = []


def main(file_name, eval_file, is_oracle_enabled):
    """
    Function: main
    Description: implements the whun algorithm
    Inputs:
    Output:
    """
    a, p, c, s, d, u, scores, t, x, e, total_cost, known_defects, features_used = [], [], [], [], [], [], [], [], [], [], [], [], []
    for i in range(20):
        print("--------------------RUN", i + 1, '------------------------')
        start_time = time.time()
        m = Method(cur_dir + '/' + cfg.whunparams["FOLDER"] + file_name, cur_dir + '/' + cfg.whunparams["FOLDER"] + eval_file)
        o = Oracle(len(m.rank))
        asked = 0
        first_qidx = set()
        while True:
            _, node = m.find_node()
            q_idx = m.pick_questions(node)
            for q in q_idx:
                first_qidx.add(q)
            asked += 1
            if not is_oracle_enabled:
                global picked_array
                picked = m.ask_questions(q_idx, node, ui_obj)
                picked_array = o.update_picked_array(picked, q_idx, node)
            else:
                picked = o.pick(q_idx, node)
            m.adjust_weights(node, picked, q_idx)
            m.re_rank()
            solutions = m.check_solution()
            if solutions is not None:
                if solutions == -1:
                    print("No solutions were found matching your preferences.")
                    a.append(asked)
                    p.append(np.sum(o.picked))
                    # c.append(-1)
                    s.append(-1)
                    d.append(-1)
                    # u.append(-1)
                    # x.append(-1)
                    # e.append(-1)
                    total_cost.append(-1)
                    known_defects.append(-1)
                    features_used.append(-1)
                    scores.append(-1)
                    t.append(time.time() - start_time)
                    break
                for item in solutions:
                    item.selectedpoints = np.sum(np.multiply(
                        item.item, o.picked)) / np.sum(o.picked) * 100
                final_solutions = semi_supervised_optimizer(
                    solutions, int(math.sqrt(len(solutions))))
                best = m.pick_best(final_solutions)
                # best = m.pick_best(solutions)
                random_s = random.choice(solutions)
                print("Found a solution.")
                a.append(asked)
                p.append(np.sum(o.picked))
                #c.append(best.effort)
                s.append(best.selectedpoints / 100)
                d.append(np.sum(o.picked)/asked)
                #u.append(best.defects)
                #x.append(best.months)
                #e.append(best.zitler_rank / 20000)
                total_cost.append(best.totalcost)
                known_defects.append(best.knowndefects)
                features_used.append(best.featuresused)
                scores.append(best.score)
                t.append(time.time() - start_time)
                break
        if not is_oracle_enabled:
            if(best != None):
                result_label = prepare_result_label(m, best, random_s)
                ui_obj.update_result_label(result_label)
                ui_obj.update_widget("ITERATION")

    df = pd.DataFrame(
        {
            'I': a,
            'S': d,
            'User Picked': p,
            # 'Effort': c,
            'Total Cost': total_cost,
            'Selected Points': s,
            'Known Defects': known_defects,
            #'Risk': d,
            # 'Defects': u,
            #'Months': x,
            'Features Used': features_used,
            'Score': scores,
            'Time': t
        }).T
    df.to_csv(cur_dir + '/' + 'Scores/Score' + file_name)


def prepare_result_label(method_obj, best_solution, random_solution):
    
    result_label = "Solution 1:\n"
    t_variable = 0	# 0 or 1
    if t_variable == 0:
        for i in range(len(best_solution.item)):
            if best_solution.item[i] == 1:
                if not len(result_label) == 0:
                    result_label+= "-> " + method_obj.questions[i] + "\n"
                else:
                    result_label = "-> " + method_obj.questions[i] + "\n"
    else:
        for i in range(len(random_solution.item)):
            if random_solution.item[i] == 1:
                if not len(result_label) == 0:
                    result_label+= "-> " + method_obj.questions[i] + "\n"
                else:
                    result_label = "-> " + method_obj.questions[i] + "\n"
    
    result_label += "Solution 2:\n"
    if t_variable == 1:
        for i in range(len(best_solution.item)):
            if best_solution.item[i] == 1:
                if not len(result_label) == 0:
                    result_label+= "-> " + method_obj.questions[i] + "\n"
                else:
                    result_label = "-> " + method_obj.questions[i] + "\n"
    else:
        for i in range(len(random_solution.item)):
            if random_solution.item[i] == 1:
                if not len(result_label) == 0:
                    result_label+= "-> " + method_obj.questions[i] + "\n"
                else:
                    result_label = "-> " + method_obj.questions[i] + "\n"
    return result_label


def sneak_run(file_names, eval_files, is_oracle_enabled=True):
    if not is_oracle_enabled:
        global ui_obj
        app = QApplication(sys.argv)
        app.setApplicationName('SneakWindow')
        ui_obj = UIHelper(app, init_process, file_names, eval_files, is_oracle_enabled)
        ui_obj.show()
        sys.exit(app.exec())
    else:
        init_process(file_names, eval_files, is_oracle_enabled)

def init_process(file_names, eval_files, is_oracle_enabled=True):
    for file, e_file in zip(file_names, eval_files):
        main(file, e_file, is_oracle_enabled)

if __name__ == "__main__":
    #sneak_run(['pom3a_bin.csv'], ['pom3a_eval.csv'], False)
    sneak_run(['Scrum10k.csv'], ['flight_eval.csv'], False)




