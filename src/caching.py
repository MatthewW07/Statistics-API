import pandas as pd
import numpy as np


class ColumnCache:
    def __init__(self, x):
        self.values = x.to_numpy()
        self.mean = self.values.mean()
        self.centered = self.values - self.mean()
        self.ss = np.dot(self.centered, self.centered)
        self.rank = x.rank().to_numpy()
        self.codes = pd.factorize(x)[0]
        self.col_vector = self.values.reshape(-1, 1)