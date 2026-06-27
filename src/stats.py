import pandas as pd
import numpy as np

"""Important Functions to Compare Data"""

# industry standard
# methods: pearson, spearman, distance, kendall, determination, nash-stucliffe
def num_v_num(x, y, cache=None) -> dict:
    if cache is None:
        cache = {}

    res = {}
    res["pearson"]   = _comp_pearson(x, y, cache={})
    print("pearson")
    res["spearman"]  = _comp_spearman(x, y, cache={})
    print("spearman")
    res["distance"]  = _comp_distance(x, y, cache={})
    print("distance")
    res["kendall"]   = _comp_kendall(x, y, cache={})
    print("kendall")
    res["determine"] = _comp_determination(x, y, cache={}, r=res["pearson"])
    print("determine")
    res["nashsut"]   = _comp_nash_sutcliffe(x, y, cache={})
    print("nashsut")
    return res

# order matters
# methods: eta, biseral, point-biseral
def num_v_cat(x, y, cache=None) -> dict:
    if cache is None:
        cache = {}

    res = {}
    res["eta"]           = _comp_eta(x, y, cache={})
    print("eta")
    res["biserial"]      = _comp_biserial(x, y, cache={})
    print("biserial")
    res["point-biseral"] = _comp_point_biserial(x, y, cache={})
    print("point-biseral")
    return res

# yeah!
# methods: cramers, cramers-unbiased, goodman-krushal
def cat_v_cat(x, y, cache=None) -> dict:
    if cache is None:
        cache = {}

    res = {}
    res["cramer"]          = _comp_cramer(x, y, cache={})
    print("cramer")
    res["cramer-unbiased"] = _comp_cramer(x, y, unbiased=True, cache={})
    print("cramer-unbiased")
    res["goodman-krushal"] = _comp_goodman_krushal(x, y, cache={})
    print("goodman-krushal")
    return res


"""Util Functions to Compare Data"""

# Number 1.
def _comp_pearson(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    x_mean = cache[x.name].mean if x.name in cache else x.mean()
    y_mean = cache[y.name].mean if y.name in cache else y.mean()

    numerator = ((x - x_mean) * (y - y_mean)).sum()
    denominator = np.sqrt(((x - x_mean) ** 2).sum() * ((y - y_mean) ** 2).sum())

    r = numerator / denominator
    return r

# Number 2.
def _comp_spearman(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    x_rank = cache[x.name].rank if x.name in cache else x.rank()
    y_rank = cache[y.name].rank if y.name in cache else y.rank()
    n = len(x)

    numerator = 6 * ((x_rank - y_rank) ** 2).sum()
    denominator = n * (n ** 2 - 1)

    rho = 1.0 - (numerator / denominator)
    return rho

# Number 3.
def _comp_distance(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    x_name = x.name
    y_name = y.name

    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    n = len(x)

    if x_name in cache:
        A_centered = cache[x_name].centered
        dvarx2 = cache[x_name].dvar2
    else:
        A = np.abs(x - x.T)
        A_mean = np.mean(A, axis=0)
        A_grand_mean = np.mean(A)
        A_centered = A - A_mean[:, np.newaxis] - A_mean[np.newaxis, :] + A_grand_mean
        dvarx2 = (A_centered * A_centered).sum() / (n ** 2)

    if y_name in cache:
        B_centered = cache[y_name].centered
        dvary2 = cache[y_name].dvar2
    else:
        B = np.abs(y - y.T)
        B_mean = np.mean(B, axis=0)
        B_grand_mean = np.mean(B)
        B_centered = B - B_mean[:, np.newaxis] - B_mean[np.newaxis, :] + B_grand_mean
        dvary2 = (B_centered * B_centered).sum() / (n ** 2)

    dcov2  = (A_centered * B_centered).sum() / (n ** 2)

    dcor = np.sqrt(dcov2) / np.sqrt(np.sqrt(dvarx2) * np.sqrt(dvary2))
    return dcor

# Number 4.
def _comp_kendall(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    return 0.0

# Number 5.
def _comp_determination(x, y, cache=None, r=None) -> float:
    if cache is None:
        cache = {}

    if r == None:
        r = _comp_pearson(x, y)
        r2 = r * r
        return r2
    else:
        return r * r

# Number 6.
# x: num, y: bin
def _comp_biserial(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    return 0.0

# Number 7.
# x: num, y: bin
def _comp_point_biserial(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    return 0.0

# Number 8.
# x: num, y: cat
def _comp_eta(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    x_mean = cache[x.name].mean if x.name in cache else x.mean()
    grouped = x.groupby(y)
    grouped_mean = grouped.mean()
    grouped_size = grouped.size()

    ss_between = (grouped_size * (grouped_mean - x_mean) ** 2).sum()
    ss_total = cache[x.name].ss if x.name in cache else ((x - x_mean) ** 2).sum()

    return np.sqrt(ss_between / ss_total)
    
# Number 9.
def _comp_nash_sutcliffe(x, y, cache=None) -> float:
    if cache is None:
        cache = {}

    return 0.0

# Number 10.
def _comp_cramer(x, y, unbiased=False, cache=None) -> float:
    if cache is None:
        cache = {}

    x_codes = cache[x.name].codes if x.name in cache else pd.factorize(x)[0]
    y_codes = cache[y.name].codes if y.name in cache else pd.factorize(y)[0]
    r = x_codes.max() + 1
    k = y_codes.max() + 1

    table = np.zeros((r, k), dtype=np.int64)
    np.add.at(table, (x_codes, y_codes), 1)
    n = table.sum()

    row_sums = table.sum(axis=1, keepdims=True)
    col_sums = table.sum(axis=0, keepdims=True)
    expected = (row_sums @ col_sums) / n

    chi2 = np.nansum(((table - expected) ** 2) / expected)
    phi2 = chi2 / n 

    if unbiased == True:
        phi2 = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        k = k - ((k - 1) ** 2) / (n - 1)
        r = r - ((r - 1) ** 2) / (n - 1)

    denominator = min(k - 1, r - 1)
    return 0.0 if denominator <= 0 else np.sqrt(phi2 / denominator)

# Number 12.
def _comp_goodman_krushal(x, y, cache=None) -> float:
    if cache is None:
        cache = {}
        
    return 0.0

# thats it!

if __name__ == "__main__":
    df = pd.read_csv("Student_Productivity_Dataset.csv")
    var_x = "Sleep_Hours_Per_Night"
    var_y = "Study_Hours_Per_Day"
    print(_comp_spearman(df[var_x], df[var_y]))