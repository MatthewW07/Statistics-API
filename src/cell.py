import pandas as pd
import numpy as np
from stats import *
from pandas.api.types import (is_numeric_dtype, is_categorical_dtype, is_bool_dtype, is_string_dtype, is_object_dtype)

class Cell:
    def __init__(self, x, y, default=None):
        self.x = x
        self.y = y
        self.comps = {}
        self.default = default
        self.type = None
        self.graphs = []

        self.classify_data()
        self.create_comps()

    def classify_variable(self, s) -> str:
        # implement heuristic stuff later cause is not good rn
        res = None
        if is_numeric_dtype(s):
            res = "num"
        elif is_categorical_dtype(s) or is_object_dtype(s) or is_bool_dtype(s) or is_string_dtype(s):
            res = "cat"
        return res
    
    def classify_data(self) -> str:
        x_type = self.classify_variable(self.x)
        y_type = self.classify_variable(self.y)

        comp_type = None
        default = None
        if x_type == "num" and y_type == "num":
            comp_type = "num_v_num"
            default = "pearson"
        elif x_type == "num" and y_type == "cat":
            comp_type = "num_v_cat"
            default = "eta"
        elif x_type == "cat" and y_type == "num":
            comp_type = "cat_v_num"
            default = "eta"
        elif x_type == "cat" and y_type == "cat":
            comp_type = "cat_v_cat"
            default = "cramer"
        self.type = comp_type
        if self.default == None: self.default = default
        return self.type
    

    def create_comps(self):
        if self.type == "num_v_num":
            self.comps = num_v_num(self.x, self.y)
        elif self.type == "num_v_cat":
            self.comps = num_v_cat(self.x, self.y)
        elif self.type == "cat_v_num":
            self.comps = num_v_cat(self.y, self.x)
        elif self.type == "cat_v_cat":
            self.comps = cat_v_cat(self.x, self.y)
        return self.comps

    def create_graphs(self):
        pass

