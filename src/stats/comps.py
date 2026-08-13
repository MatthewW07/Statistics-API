import pandas as pd
import numpy as np
from src.stats.two_var import *


""" The functions to compare two variables """


# Methods: Pearson, Spearman, Distance, Kendall, Determination, Nash-Stucliffe
def num_v_num(x, y, cache=None) -> dict:
    if cache is None: cache = {}
    res = {}
    res["pearson"] = comp_pearson(x, y, cache=cache)
    res["spearman"] = comp_spearman(x, y, cache=cache)
    res["distance"] = comp_distance(x, y, cache=cache)
    res["kendall"] = comp_kendall(x, y, cache=cache)
    res["determine"] = comp_determination(x, y, cache=cache, r=res["pearson"])
    res["nashsut"] = comp_nash_sutcliffe(x, y, cache=cache)
    return res


# Methods: Eta, Biseral, Point-Biseral
def num_v_cat(x, y, cache=None) -> dict:
    if cache is None: cache = {}
    res = {}
    res["eta"] = comp_eta(x, y, cache=cache)
    res["biserial"] = comp_biserial(x, y, cache=cache)
    res["point-biseral"] = comp_point_biserial(x, y, cache=cache)
    return res


# Methods: Cramers, Cramers-Unbiased, Goodman-Krushal
def cat_v_cat(x, y, cache=None) -> dict:
    if cache is None: cache = {}
    res = {}
    res["cramer"] = comp_cramer(x, y, cache=cache)
    res["cramer-unbiased"] = comp_cramer(x, y, unbiased=True, cache=cache)
    res["goodman-krushal"] = comp_goodman_krushal(x, y, cache=cache)
    return res


# For testing
if __name__ == "__main__":
    df = pd.read_csv("Student_Productivity_Dataset.csv")
    var_x = "Sleep_Hours_Per_Night"
    var_y = "Study_Hours_Per_Day"
    print(comp_spearman(df[var_x], df[var_y]))
