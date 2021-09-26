from csv import reader
import sys
sys.path.append('/whun_helper')
from whun_helper.Item import Item
import pandas as pd
import configparams as cfg
class SATSolver:

    @staticmethod
    def get_solutions(cnf, eval_file):
        global folder
        #global eval_file
        evals = pd.read_csv(cfg.whunparams["FOLDER"] + eval_file).to_numpy()

        with open(cnf, 'r') as read_obj:
            binary_solutions = [[int(x) for x in rec]
                                for rec in reader(read_obj, delimiter=',')]
            items = []
            for i, item in enumerate(binary_solutions):
                items.append(Item(item, evals[i]))
            return items

