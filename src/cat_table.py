
import pandas as pd
import numpy as np
from src.stats.utils import classify_variable
from src.consts import categoric_table_columns

class Categorical_Table:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.columns = categoric_table_columns
        self.variables = []
        self.stats = {}
        self.n = 0

        # Get the categorical variables/columns
        self.get_categoric_variables()

        # Fill in the table
        self.create_table()


    def get_categoric_variables(self):
        categoric_variables = []
        for column in self.df.columns:
            if classify_variable(self.df[column]) != "num":
                categoric_variables.append(column)
        self.variables = categoric_variables
        self.n = len(categoric_variables)


    def create_table(self):
        for v in self.variables:
            self.get_stats(v)


    def get_stats(self, v):
        self.stats[v] = {}
        self.stats[v]["cnt"] = self.df[v].count()
        self.stats[v]["missing_cnt"] = self.df[v].isnull().sum()
        self.stats[v]["missing_pct"] = (self.df[v].isnull().sum() / len(self.df[v])) * 100
        self.stats[v]["categories"] = self.df[v].value_counts().to_dict()
        self.stats[v]["mode"] = self.df[v].mode()[0] if not self.df[v].mode().empty else np.nan
        self.stats[v]["mode_cnt"] = self.df[v].value_counts().iloc[0] if not self.df[v].value_counts().empty else np.nan
        self.stats[v]["mode_pct"] = (self.df[v].value_counts().iloc[0] / len(self.df[v])) * 100 if not self.df[v].value_counts().empty else np.nan
        self.stats[v]["second_mode"] = self.df[v].value_counts().index[1] if len(self.df[v].value_counts()) > 1 else np.nan
        self.stats[v]["second_mode_cnt"] = self.df[v].value_counts().iloc[1] if len(self.df[v].value_counts()) > 1 else np.nan
        self.stats[v]["second_mode_pct"] = (self.stats[v]["second_mode_cnt"] / len(self.df[v])) * 100 if len(self.df[v].value_counts()) > 1 else np.nan
        self.stats[v]["least_frequent"] = self.df[v].value_counts().index[-1] if len(self.df[v].value_counts()) > 0 else np.nan
        self.stats[v]["least_frequent_cnt"] = self.df[v].value_counts().iloc[-1] if len(self.df[v].value_counts()) > 0 else np.nan
        self.stats[v]["least_frequent_pct"] = (self.stats[v]["least_frequent_cnt"] / len(self.df[v])) * 100 if len(self.df[v].value_counts()) > 0 else np.nan
        self.stats[v]["entropy"] = -(self.df[v].value_counts(normalize=True) * np.log2(self.df[v].value_counts(normalize=True))).sum()
        self.stats[v]["normalized_entropy"] = self.stats[v]["entropy"] / np.log2(len(self.df[v].value_counts())) if len(self.df[v].value_counts()) > 1 else np.nan
        self.stats[v]["concentration_ratio"] = self.stats[v]["mode_cnt"] / len(self.df[v]) if len(self.df[v]) > 0 else np.nan
