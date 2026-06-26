import pandas
import numpy

# 4 more global functions


# industry standard
def num_v_num(x, y, method="pearson"):
    pass

# order matters
def num_v_cat(x, y, method="eta"):
    pass

# yeah!
def cat_v_cat(x, y, method="cramer"):
    pass


# 11 comparison coefficients to implement...

def _comp_pearson(x, y) -> float:
    pass

def _comp_spearman(x, y) -> float:
    pass

def _comp_distance(x, y) -> float:
    pass

def _comp_kendall(x, y) -> float:
    pass

def _comp_determination(x, y) -> float:
    pass

def _comp_biserial(x, y) -> float:
    pass

def _comp_point_biserial(x, y) -> float:
    pass

# x: num, y: cat
def _comp_eta(x, y) -> float:
    pass

def _comp_nash_sutcliffe(x, y) -> float:
    pass

def _comp_cramer(x, y, unbiased=True) -> float:
    pass

def _comp_goodman_krushal(x, y) -> float:
    pass

# thats it!