
import pandas as pd
import numpy as np
from src.stats.utils import classify_column

class Numerical_Table:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.columns = []
        self.n = 0


    def get_numeric_columns(self):
        numeric_columns = []
        for column in self.df.columns:
            if classify_column(self.df[column]) == "num":
                numeric_columns.append(column)
        self.columns = numeric_columns
        self.n = len(numeric_columns)


    def create_table(self):
        pass


