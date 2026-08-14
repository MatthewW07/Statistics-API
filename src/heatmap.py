import pandas as pd
import numpy as np
from src.stats.comparisons import *
from src.cell import Cell
from src.stats.caching import VariableCache
from src.stats.utils import classify_variable
from typing import Tuple

class Heatmap:
    def __init__(self, file_path, defaults={"num_v_num": "pearson", "num_v_cat": "eta", "cat_v_cat": "cramer"}):
        self.df = pd.read_csv(file_path)
        self.m = self.df.shape[0]
        self.n = self.df.shape[1]
        self.heatmap = [[None for _ in range(self.n)] for _ in range(self.n)]
        self.corr_matrix = [[0.0 for _ in range(self.n)] for _ in range(self.n)]
        self.variables = self.df.columns
        self.types = {}
        self.defaults = defaults
        self.column_cache = {}

        # Classifying
        self.classify_columns()

        # Create Caches
        self.create_caches()

        # Create Heatmap
        self.create_heatmap()

        # Create Correlation Matrix
        self.create_corr_matrix()


    # Used to classify every variable/column as Numerical or Categorical
    # Eventually, it should be able to further classify Categorical variables/columns 
    # as binary, ordinal, nominal, id/label, etc.
    # Currently, it only labels as "num" or "cat"
    def classify_variables(self) -> dict:
        # Maps the variable/column type to the dictionary self.types
        # Key to Value is "variable : type"
        res = {}
        for var, s in self.df.items():
            res[var] = classify_variable(s)
        self.types = res
        return self.types
        

    # Create caches for each variable/colums
    def create_caches(self):
        for variable in self.variables:
            self.column_cache[variable] = VariableCache(self.df[variable])

    
    # Creates the main heatmap, which is a 2D m by n array of Cell objects
    def create_heatmap(self) -> np.ndarray[Tuple[int, int], np.dtype[np.float64]]:
        for i in range(self.n):
            for j in range(i, self.n):
                x = self.df[self.variables[i]]
                y = self.df[self.variables[j]]

                cell = Cell(x, y, column_cache=self.column_cache)
                self.heatmap[i][j] = cell
                self.heatmap[j][i] = cell.flip_cell()

        return self.heatmap


    # Creates a Correlation Matrix, which is a 2D m by n array of floats
    # The Correlation Matrix is essentially a bare version of the Heatmap
    def create_corr_matrix(self):
        for i in range(self.n):
            for j in range(i, self.n):
                cell = self.heatmap[i][j]
                comp_type = cell.type
                
                if comp_type == "num_v_num":
                    value = cell.comps[self.defaults["num_v_num"]]
                elif comp_type in ["num_v_cat", "cat_v_num"]:
                    value = cell.comps[self.defaults["num_v_cat"]]
                elif comp_type == "cat_v_cat":
                    value = cell.comps[self.defaults["cat_v_cat"]]
                else:
                    value = np.nan
                self.corr_matrix[i][j] = value
                self.corr_matrix[j][i] = value
        
        return self.corr_matrix


if __name__ == "__main__":
    heatmap = Heatmap("Student_Productivity_Dataset.csv")
    print(heatmap.corr_matrix)
    