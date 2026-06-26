import pandas as pd
import numpy as np

"""Important Functions to Compare Data"""

# industry standard
# methods: pearson, spearman, distance, kendall, determination, nash-stucliffe
def num_v_num(x, y) -> dict:
    res = {}
    res["pearson"]   = _comp_pearson(x, y)
    res["spearman"]  = _comp_spearman(x, y)
    res["distance"]  = _comp_distance(x, y)
    res["kendall"]   = _comp_kendall(x, y)
    res["determine"] = _comp_determination(x, y)
    res["nashsut"]   = _comp_nash_sutcliffe(x, y)
    return res

# order matters
# methods: eta, biseral, point-biseral
def num_v_cat(x, y) -> dict:
    res = {}
    res["eta"]           = _comp_eta(x, y)
    res["biserial"]      = _comp_biserial(x, y)
    res["point-biseral"] = _comp_point_biserial(x, y)
    return res

# yeah!
# methods: cramers, cramers-unbiased, goodman-krushal
def cat_v_cat(x, y) -> dict:
    res = {}
    res["cramer"]          = _comp_cramer(x, y)
    res["cramer-unbiased"] = _comp_cramer_unbiased(x, y)
    res["goodman-krushal"] = _comp_goodman_krushal(x, y)
    return res


"""Important Function to Classify Data"""

def classify(x):
    pass


"""Util Functions to Compare Data"""

# Number 1.
def _comp_pearson(x, y) -> float:
    x_mean = x.mean()
    y_mean = y.mean()

    numerator = ((x - x_mean) * (y - y_mean)).sum()
    denominator = np.sqrt(((x - x_mean) ** 2).sum() * ((y - y_mean) ** 2).sum())

    r = numerator / denominator
    return r

# Number 2.
def _comp_spearman(x, y) -> float:
    x_rank = x.rank()
    y_rank = y.rank()
    n = len(x)

    numerator = 6 * ((x_rank - y_rank) ** 2).sum()
    denominator = n * (n ** 2 - 1)

    rho = 1.0 - (numerator / denominator)
    return rho

# Number 3.
def _comp_distance(x, y) -> float:
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    n = len(x)

    A = np.abs(x - x.T)
    B = np.abs(y - y.T)

    A_mean = np.mean(A, axis=0)
    B_mean = np.mean(B, axis=0)

    A_grand_mean = np.mean(A)
    B_grand_mean = np.mean(B)

    A_centered = A - A_mean[:, np.newaxis] - A_mean[np.newaxis, :] + A_grand_mean
    B_centered = B - B_mean[:, np.newaxis] - B_mean[np.newaxis, :] + B_grand_mean

    dcov2  = (A_centered * B_centered).sum() / (n ** 2)
    dvarx2 = (A_centered * A_centered).sum() / (n ** 2)
    dvary2 = (B_centered * B_centered).sum() / (n ** 2)

    dcor = np.sqrt(dcov2) / np.sqrt(np.sqrt(dvarx2) * np.sqrt(dvary2))
    return dcor

# Number 4.
def _comp_kendall(x, y) -> float:
    # shhhhhhhh
    tau = x.corr(y, method="kendall")
    return tau

# Number 5.
def _comp_determination(x, y) -> float:
    r = _comp_pearson(x, y)
    r2 = r * r
    return r2

# Number 6.
def _comp_biserial(x, y) -> float:
    pass

# Number 7.
def _comp_point_biserial(x, y) -> float:
    pass

# Number 8.
# x: num, y: cat
def _comp_eta(x, y) -> float:
    x_mean = x.mean()
    grouped = x.groupby(y)
    grouped_mean = grouped.mean()
    grouped_size = grouped.size()

    ss_between = (grouped_size * (grouped_mean - x_mean) ** 2).sum()
    ss_total = ((x - x_mean) ** 2).sum()

    return np.sqrt(ss_between / ss_total)
    
# Number 9.
def _comp_nash_sutcliffe(x, y) -> float:
    pass

# Number 10.
def _comp_cramer(x, y) -> float:
    x_codes, _ = pd.factorize(x)
    y_codes, _ = pd.factorize(y)
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

    phi2corr = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r-1) ** 2) / (n - 1)
    kcorr = k - ((k-1) ** 2) / (n - 1)

    denominator = min(kcorr - 1, rcorr - 1)
    return 0.0 if denominator <= 0 else np.sqrt(phi2corr / denominator)

# Number 11.
def _comp_cramer_unbiased(x, y) -> float:
    pass

# Number 12.
def _comp_goodman_krushal(x, y) -> float:
    pass

# thats it!

if __name__ == "__main__":
    df = pd.read_csv("Student_Productivity_Dataset.csv")
    var_x = "Sleep_Hours_Per_Night"
    var_y = "Study_Hours_Per_Day"
    print(_comp_spearman(df[var_x], df[var_y]))