""" Basic Caches for each column in a DataFrame """

import numpy as np
import pandas as pd

class ColumnCache:
    """Column-level values that remain valid when a comparison uses every row.

    Pairwise statistics must not reuse these values after either input has had
    missing rows removed; ``utils`` checks ``source_length`` before using them.
    """

    def __init__(self, x):
        self.name = x.name
        self.source_length = len(x)
        self.dtype = x.dtype
        self.is_numeric = pd.api.types.is_numeric_dtype(x)
        self.is_categoric = (
            isinstance(x.dtype, pd.CategoricalDtype)
            or pd.api.types.is_object_dtype(x)
            or pd.api.types.is_bool_dtype(x)
            or pd.api.types.is_string_dtype(x)
        )

        if self.is_numeric:
            self.values = pd.to_numeric(x, errors="coerce").to_numpy(dtype=float)
            self.valid_count = int(np.isfinite(self.values).sum())
            self.mean = float(np.nanmean(self.values)) if self.valid_count else np.nan
            self.centered = self.values - self.mean
            self.ss = float(np.nansum(self.centered ** 2))
            self.rank = x.rank(method="average")

        if self.is_categoric:
            self.codes, self.categories = pd.factorize(x, sort=False)
