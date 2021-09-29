"""This module is related to SAT Solver Class"""
# pylint: disable=import-error,invalid-name
import sys
from csv import reader
import pandas as pd
import configparams as cfg
from whun_helper.item import Item

sys.path.append('/whun_helper')

class sat_solver:
    """This class is used for getting """
    @staticmethod
    def get_solutions(cnf, eval_file):
        """
        Function: get_solutions
        Description: Takes CNF and evaluation metrics and returns list of Item class objects
        Inputs:
            -cnf:String
            -eval_file:String
        Output:
            -items :Item
        """
        #global folder
        #global eval_file
        evals = pd.read_csv(cfg.whunparams["FOLDER"] + eval_file).to_numpy()

        with open(cnf, 'r') as read_obj:
            binary_solutions = [[int(x) for x in rec]
                                for rec in reader(read_obj, delimiter=',')]
            items = []
            for i, item in enumerate(binary_solutions):
                items.append(Item(item, evals[i]))
            return items
