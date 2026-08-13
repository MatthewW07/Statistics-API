
import pandas as pd
import numpy as np
from src.stats.utils import classify_column

class Numerical_Table:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.columns = []
        self.stats = {}
        self.n = 0

        # Get the numerical variables/columns
        self.get_numeric_columns(self)

        # Fill in the table
        self.create_table(self)


    def get_numeric_columns(self):
        numeric_columns = []
        for column in self.df.columns:
            if classify_column(self.df[column]) == "num":
                numeric_columns.append(column)
        self.columns = numeric_columns
        self.n = len(numeric_columns)


    def create_table(self):
        for column in self.columns:
            self.get_stats(column)


    def get_stats(self, column):
        self.stats[column] = {}
        self.stats[column]["mean"] = self.df[column].mean()
        self.stats[column]["median"] = self.df[column].median()
        self.stats[column]["std_dev"] = self.df[column].std()
        self.stats[column]["var"] = self.df[column].var()
        self.stats[column]["min"] = self.df[column].min()
        self.stats[column]["max"] = self.df[column].max()
        self.stats[column]["range"] = self.df[column].max() - self.df[column].min()
        self.stats[column]["p5"] = self.df[column].quantile(0.05)
        self.stats[column]["p10"] = self.df[column].quantile(0.10)
        self.stats[column]["p25"] = self.df[column].quantile(0.25)
        self.stats[column]["p75"] = self.df[column].quantile(0.75)
        self.stats[column]["p90"] = self.df[column].quantile(0.90)
        self.stats[column]["p95"] = self.df[column].quantile(0.95)
        self.stats[column]["iqr"] = self.df[column].quantile(0.75) - self.df[column].quantile(0.25)
        self.stats[column]["skew"] = self.df[column].skew()
        self.stats[column]["kurtosis"] = self.df[column].kurtosis()
        self.stats[column]["mad"] = self.df[column].mad()
        self.stats[column]["sem"] = self.df[column].sem()
        self.stats[column]["cv"] =(self.df[column].std() / self.df[column].mean()) * 100
        self.stats[column]["mean_ci_95_low"] =self.df[column].mean() - 1.96 * (self.df[column].std() / np.sqrt(len(self.df[column])))
        self.stats[column]["mean_ci_95_high"] =self.df[column].mean() + 1.96 * (self.df[column].std() / np.sqrt(len(self.df[column])))

