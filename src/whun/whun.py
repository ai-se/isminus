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

random.seed(datetime.now())


def main(file_name, eval_file):
    """
    Function: main
    Description: implements the whun algorithm
    Inputs:
    Output:
    """
    a, p, c, s, d, u, scores, t, x, e, total_cost, known_defects, features_used = [], [], [], [], [], [], [], [], [], [], [], [], []
    for i in range(100):
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
            m.ask_questions(q_idx, node)
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


if __name__ == "__main__":
    filenames = ['Scrum10k.csv']
    eval_files = ['flight_eval.csv']
    for file, e_file in zip(filenames, eval_files):
        main(file, e_file)


def whun_run(file_names, eval_files):
    for file, e_file in zip(file_names, eval_files):
        main(file, e_file)
