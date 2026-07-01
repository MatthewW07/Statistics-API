import pandas as pd
import numpy as np


class ColumnCache:
    def __init__(self, x):
        self.name = x.name
        self.values = x.to_numpy()
        self.n = len(x)

        if x.dtype == "float64" or x.dtype == "int64":
            self.mean = self.values.mean()
            self.centered = self.values - self.mean
            self.ss = np.dot(self.centered, self.centered)
            self.rank = x.rank().to_numpy()

            x_col = np.array(x).reshape(-1, 1)
            A = np.abs(x_col - x_col.T)
            A_mean = np.mean(A, axis=0)
            A_grand_mean = np.mean(A)
            self.centered = A - A_mean[:, np.newaxis] - A_mean[np.newaxis, :] + A_grand_mean
            self.dvar2 = (self.centered * self.centered).sum() / (self.n ** 2)

        if x.dtype == "object" or x.dtype == "category":
            self.codes = pd.factorize(x)[0]
            self.unique_codes = np.unique(self.codes)
            


