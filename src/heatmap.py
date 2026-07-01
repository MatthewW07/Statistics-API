import pandas as pd
import numpy as np
from stats import *
from cell import Cell
from typing import Tuple
from caching import ColumnCache
from pandas.api.types import (
    is_numeric_dtype, is_bool_dtype, is_categorical_dtype, is_object_dtype, is_string_dtype
)

class Heatmap:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        m, n = self.df.shape
        self.m = m
        self.n = n
        self.full_matrix = [[None for _ in range(self.n)] for _ in range(self.n)]
        self.corr_matrix = [[0.0 for _ in range(self.n)] for _ in range(self.n)]
        self.columns = self.df.columns
        self.types = {}
        self.caches = {}

    def create_caches(self):
        for i in range(self.n):
            x = self.df[self.columns[i]]
            name = x.name
            self.caches[name] = ColumnCache(x)

    def classify_column(self, s) -> str:
        # implement heuristic stuff later cause is not good rn
        res = None
        if is_numeric_dtype(s):
            res = "num"
        elif is_categorical_dtype(s) or is_object_dtype(s) or is_bool_dtype(s) or is_string_dtype(s):
            res = "cat"
        return res

    def classify_all_columns(self) -> dict:
        # maps all column to type ("num" or "cat" so far)
        res = {}
        for var, s in self.df.items():
            res[var] = self.classify_column(s)
        self.types = res
        return self.types

    def create_full_matrix(self) -> np.ndarray[Tuple[int, int], np.dtype[np.float64]]:
        # idk how make this better, but oh well it's not like they have 10^5 columns
        for i in range(self.n):
            print(f"On {i} of {self.n} for full matrix")
            for j in range(i, self.n):
                x = self.df[self.columns[i]]
                y = self.df[self.columns[j]]

                cell = Cell(x, y, cache=self.caches)
                self.full_matrix[i][j] = cell
                cell.flip_cell()
                self.full_matrix[j][i] = cell

        return self.full_matrix
        # makes a bunch of Cell objects

    def create_corr_matrix(self, num_v_num="pearson", num_v_cat="eta", cat_v_cat="cramer"):
        for i in range(self.n):
            print(f"On {i} of {self.n} for corr matrix")
            for j in range(i, self.n):
                x = self.df[self.columns[i]]
                y = self.df[self.columns[j]]
                cell = self.full_matrix[i][j]
                comp_type = cell.type

                if comp_type == "num_v_num":
                    self.corr_matrix[i][j] = cell.comps[num_v_num]
                if comp_type in ["num_v_cat", "cat_v_num"]:
                    self.corr_matrix[i][j] = cell.comps[num_v_cat]
                if comp_type == "cat_v_cat":
                    self.corr_matrix[i][j] = cell.comps[cat_v_cat]
        
        return self.corr_matrix


if __name__ == "__main__":
    heatmap = Heatmap("Student_Productivity_Dataset.csv")
    print("Creating caches...")
    heatmap.create_caches()
    print("Creating full matrix...")
    heatmap.create_full_matrix()
    # print(len(heatmap.full_matrix), len(heatmap.full_matrix[0]))
    print("Creating correlation matrix...")
    heatmap.create_corr_matrix()
    print(heatmap.corr_matrix)
    