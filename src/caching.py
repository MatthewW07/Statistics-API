import pandas as pd
import numpy as np


class ColumnCache:
    def __init__(self, x):
        self.name = x.name
        self.values = x.to_numpy()
        self.n = len(x)
        self.mean = self.values.mean() if x.dtype == "float" else None
        self.centered = self.values - self.mean if x.dtype == "float" else None
        self.ss = np.dot(self.centered, self.centered) if x.dtype == "float" else None
        self.rank = x.rank().to_numpy() if x.dtype == "float" else None
        self.codes = pd.factorize(x)[0] if x.dtype == "object" else None

        if x.dtype == "float":
            x_col = np.array(x).reshape(-1, 1)
            A = np.abs(x_col - x_col.T)
            A_mean = np.mean(A, axis=0)
            A_grand_mean = np.mean(A)
            self.centered = A - A_mean[:, np.newaxis] - A_mean[np.newaxis, :] + A_grand_mean
            self.dvar2 = (self.centered * self.centered).sum() / (self.n ** 2)


