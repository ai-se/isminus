"""This module is related to WHUN implementation"""
import os
import random
import sys
import time
from datetime import datetime
import numpy as np
import pandas as pd
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)
from config import configparams as cfg
from whun_helper.method import Method
from whun_helper.oracle import Oracle
from whun_helper.ui_helper import UIHelper
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
    for i in range(1):
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
                    # d.append(-1)
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
                best = m.pick_best(solutions)
                print("Found a solution.")
                a.append(asked)
                p.append(np.sum(o.picked))
                #c.append(best.effort)
                s.append(best.selectedpoints / 100)
                #d.append(best.risk)
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
            result_label = prepare_result_label(m)
            ui_obj.update_result_label(result_label)
            ui_obj.update_widget("ITERATION")

    df = pd.DataFrame(
        {
            'Asked': a,
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
            # 'Pure Score': e,
            'Time': t
        }).T
    df.to_csv(cur_dir + '/' + 'Scores/Score' + file_name)


def prepare_result_label(method_obj):
    result_label = ""
    for i in range(len(picked_array)):
        if picked_array[i] == 1:
            if not len(result_label) == 0:
                result_label+= "-> " + method_obj.questions[i] + "\n"
            else:
                result_label = "-> " + method_obj.questions[i] + "\n"
    return result_label


def whun_run(file_names, eval_files, is_oracle_enabled=True):
    for file, e_file in zip(file_names, eval_files):
        main(file, e_file, is_oracle_enabled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('WhunWindow')
    ui_obj = UIHelper(app, whun_run)
    ui_obj.show()
    sys.exit(app.exec())


