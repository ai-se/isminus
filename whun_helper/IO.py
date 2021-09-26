import pandas as pd
import configparams as cfg


class IO:

    @staticmethod
    def read_dimacs(filename):
        file = open(filename)
        lines = file.readlines()
        names = []
        for line in lines[:cfg.whunparams["NUM_FEATURES"]]:
            names.append(line.split(' ')[2][:-1])
        dimacs = lines[cfg.whunparams["NUM_FEATURES"] + 1:]
        cnf = [[int(s) for s in line.split(' ') if int(s) != 0]
               for line in dimacs]
        return names, cnf

    @staticmethod
    def get_question_text(filename, column):
        df = pd.read_csv(filename)
        return df[column].tolist()
