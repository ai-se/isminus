import random
import sys
import time
from datetime import datetime
import numpy as np
import pandas as pd
import configparams as cfg
from whun_helper.Method import Method
from whun_helper.oracle import Oracle
sys.path.append('/whun_helper')

# SETUP VARIABLES

# TODO: to be removed after all the refactor
filename = ''
eval_file = ''

random.seed(datetime.now())

def main():
    global filename
    global eval_file
    a, p, c, s, d, u, scores, t, x, e = [], [], [], [], [], [], [], [], [], []
    for i in range(5):
        print("--------------------RUN", i + 1, '------------------------')
        start_time = time.time()
        m = Method(cfg.whunparams["FOLDER"] + filename, eval_file)
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
