import pandas as pd
import numpy as np
from stats import *
from cell import Cell
from typing import Tuple
from pandas.api.types import (is_numeric_dtype, is_categorical_dtype, is_bool_dtype, is_string_type, is_object_type)

class Heatmap:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        m, n = self.df.shape()
        self.m = m
        self.n = n
        self.matrix = [[None for _ in range(self.n)] for _ in range(self.m)]
        self.columns = self.df.columns
        self.types = {}

    def classify_column(self, s) -> str:
        # implement heuristic stuff later cause is not good rn
        res = None
        if is_numeric_dtype(s):
            res = "num"
        elif is_categorical_dtype(s) or is_object_type(s) or is_bool_dtype(s) or is_string_type(s):
            res = "cat"
        return res

    def classify_columns(self) -> dict:
        # maps all column to type ("num" or "cat" so far)
        res = {}
        for var, s in self.df.items():
            res[var] = self.classify_column(s)
        self.types = res
        return self.types

    def create_matrix(self, num_v_num="pearson", num_v_cat="eta", cat_v_cat="cramer") -> np.ndarray[Tuple[int, int], np.dtype[np.float64]]:
        # idk how make this better, but oh well it's not like they have 10^5 columns
        for i in range(self.n):
            for j in range(i, self.n):
                x = self.df[self.columns[i]]
                y = self.df[self.columns[j]]

                self.matrix[i][j] = Cell(self.df, x, y)
                self.matrix[j][i] = Cell(self.df, x, y)


        return self.matrix
        # makes a bunch of Cell objects


# meh