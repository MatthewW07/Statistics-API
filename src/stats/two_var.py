
import math
import numpy as np
import pandas as pd
from src.stats.utils import numeric_pair, mixed_pair

def comp_pearson(x, y, cache=None) -> float:
    x, y = numeric_pair(x, y)
    if len(x) < 2:
        return np.nan
    # Means cached from the original columns are safe only when no pairwise rows
    # were removed.  The sums below are intentionally computed on the pair.
    x_centered = x - x.mean()
    y_centered = y - y.mean()
    denominator = math.sqrt(float((x_centered**2).sum() * (y_centered**2).sum()))
    return np.nan if denominator == 0 else float((x_centered * y_centered).sum() / denominator)


def comp_spearman(x, y, cache=None) -> float:
    x, y = numeric_pair(x, y)
    if len(x) < 2:
        return np.nan
    return comp_pearson(x.rank(method="average"), y.rank(method="average"))


def comp_distance(x, y, cache=None, max_samples=1000) -> float:
    """Distance correlation, using an evenly spaced sample for large inputs.

    Exact distance correlation requires an n-by-n matrix.  Capping the sample
    prevents a 10,000-row input from allocating gigabytes for every heatmap cell.
    """
    x, y = numeric_pair(x, y)
    n = len(x)
    if n < 2:
        return np.nan
    if n > max_samples:
        positions = np.linspace(0, n - 1, max_samples, dtype=int)
        x, y, n = x.iloc[positions], y.iloc[positions], max_samples
    xv, yv = x.to_numpy(dtype=float), y.to_numpy(dtype=float)
    a = np.abs(xv[:, None] - xv[None, :])
    b = np.abs(yv[:, None] - yv[None, :])
    a -= a.mean(axis=0)[None, :]
    a -= a.mean(axis=1)[:, None]
    a += a.mean()
    b -= b.mean(axis=0)[None, :]
    b -= b.mean(axis=1)[:, None]
    b += b.mean()
    dcov2 = float((a * b).mean())
    dvarx2, dvary2 = float((a * a).mean()), float((b * b).mean())
    if dvarx2 <= 0 or dvary2 <= 0:
        return np.nan
    return float(math.sqrt(max(dcov2, 0.0) / math.sqrt(dvarx2 * dvary2)))


def comp_kendall(x, y, cache=None) -> float:
    x, y = numeric_pair(x, y)
    return np.nan if len(x) < 2 else float(x.corr(y, method="kendall"))


def comp_determination(x, y, cache=None, r=None) -> float:
    r = comp_pearson(x, y, cache=cache) if r is None else r
    return np.nan if not np.isfinite(r) else float(r * r)


def _binary_pair(x, y):
    x, y = mixed_pair(x, y)
    levels = pd.unique(y)
    if len(levels) != 2 or len(x) < 2:
        return None, None
    codes = (y == levels[1]).to_numpy(dtype=bool)
    return x.to_numpy(dtype=float), codes


def comp_point_biserial(x, y, cache=None) -> float:
    values, codes = _binary_pair(x, y)
    if values is None:
        return np.nan
    p = codes.mean()
    q = 1.0 - p
    std = values.std(ddof=1)
    if p == 0 or q == 0 or std == 0:
        return np.nan
    return float((values[codes].mean() - values[~codes].mean()) / std * math.sqrt(p * q))


def _normal_ppf(p):
    """Inverse standard-normal CDF (Acklam rational approximation)."""
    if not 0.0 < p < 1.0:
        return np.nan
    a = (-39.6968302866538, 220.946098424521, -275.928510446969, 138.357751867269, -30.6647980661472, 2.50662827745924)
    b = (-54.4760987982241, 161.585836858041, -155.698979859887, 66.8013118877197, -13.2806815528857)
    c = (-0.00778489400243029, -0.322396458041136, -2.40075827716184, -2.54973253934373, 4.37466414146497, 2.93816398269878)
    d = (0.00778469570904146, 0.32246712907004, 2.445134137143, 3.75440866190742)
    if p < 0.02425:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)
    if p > 0.97575:
        return -_normal_ppf(1.0 - p)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1.0)


def comp_biserial(x, y, cache=None) -> float:
    values, codes = _binary_pair(x, y)
    if values is None:
        return np.nan
    r_pb = comp_point_biserial(x, y, cache=cache)
    p, q = codes.mean(), 1.0 - codes.mean()
    if not np.isfinite(r_pb) or p == 0 or q == 0:
        return np.nan
    # Biserial correction for an underlying normally distributed split variable.
    z = abs(_normal_ppf(q))
    height = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    return float(r_pb * math.sqrt(p * q) / height)


def comp_eta(x, y, cache=None) -> float:
    x, y = mixed_pair(x, y)
    if len(x) < 2:
        return np.nan
    overall_mean = x.mean()
    grouped = x.groupby(y, observed=False)
    ss_between = float((grouped.size() * (grouped.mean() - overall_mean) ** 2).sum())
    ss_total = float(((x - overall_mean) ** 2).sum())
    return np.nan if ss_total == 0 else float(math.sqrt(ss_between / ss_total))


def comp_nash_sutcliffe(x, y, cache=None) -> float:
    x, y = numeric_pair(x, y)
    if len(x) < 2:
        return np.nan
    denominator = float(((y - y.mean()) ** 2).sum())
    return np.nan if denominator == 0 else float(1.0 - ((x - y) ** 2).sum() / denominator)


def comp_cramer(x, y, unbiased=False, cache=None) -> float:
    df = pd.concat([pd.Series(x), pd.Series(y)], axis=1).dropna()
    if len(df) < 2:
        return np.nan
    table = pd.crosstab(df.iloc[:, 0], df.iloc[:, 1]).to_numpy(dtype=float)
    n = table.sum()
    r, k = table.shape
    if r < 2 or k < 2:
        return np.nan
    expected = np.outer(table.sum(axis=1), table.sum(axis=0)) / n
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = float(np.divide((table - expected) ** 2, expected, out=np.zeros_like(table), where=expected > 0).sum())
    phi2 = chi2 / n
    if unbiased:
        phi2 = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        r -= (r - 1) ** 2 / (n - 1)
        k -= (k - 1) ** 2 / (n - 1)
    denominator = min(k - 1, r - 1)
    return np.nan if denominator <= 0 else float(math.sqrt(phi2 / denominator))


def comp_goodman_krushal(x, y, cache=None) -> float:
    """Symmetric Goodman--Kruskal lambda (average predictive reduction in error)."""
    df = pd.concat([pd.Series(x), pd.Series(y)], axis=1).dropna()
    if len(df) < 2:
        return np.nan
    table = pd.crosstab(df.iloc[:, 0], df.iloc[:, 1]).to_numpy(dtype=int)

    def directional_error_reduction(t):
        e1 = t.sum() - t.sum(axis=0).max()
        e2 = sum(row.sum() - row.max() for row in t)
        return np.nan if e1 == 0 else (e1 - e2) / e1

    values = [directional_error_reduction(table), directional_error_reduction(table.T)]
    values = [v for v in values if np.isfinite(v)]
    return np.nan if not values else float(np.mean(values))
