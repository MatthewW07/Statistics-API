import pandas as pd
import numpy as np
from stats import *

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.comps = {}
        self.default = ""
        self.graphs = []

    def classify_data(self):
        pass

    def create_comps(self):
        pass

    def create_graphs(self):
        pass

    def create_meta_data(self):
        pass
