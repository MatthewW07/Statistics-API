"""Association statistics used by the heatmap."""

import math
import numpy as np
import pandas as pd
from pandas.api.types import (
    is_numeric_dtype, is_bool_dtype, is_categorical_dtype, is_object_dtype, is_string_dtype
)


def cache_get(cache, key, attr, default, *, length=None):
    """Read a cache entry only when it describes the same complete sample."""
    if cache is None or key not in cache:
        return default()
    entry = cache[key]
    if length is not None and getattr(entry, "source_length", length) != length:
        return default()
    if isinstance(entry, dict):
        return entry.get(attr, default())
    return getattr(entry, attr, default())


def numeric_pair(x, y):
    df = pd.concat([pd.Series(x), pd.Series(y)], axis=1)
    df = df.apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return df.iloc[:, 0], df.iloc[:, 1]


def mixed_pair(x, y):
    df = pd.concat([pd.Series(x), pd.Series(y)], axis=1).dropna()
    if df.empty:
        return pd.Series(dtype=float), pd.Series(dtype=object)
    numeric = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    mask = np.isfinite(numeric)
    return numeric[mask], df.iloc[:, 1][mask]


def classify_variable(s) -> str:
    res = ""
    if is_numeric_dtype(s):
        res = "num"
    elif is_categorical_dtype(s) or is_object_dtype(s) or is_bool_dtype(s) or is_string_dtype(s):
        res = "cat"
    return res