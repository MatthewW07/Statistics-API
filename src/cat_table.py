
import pandas as pd
import numpy as np
from src.stats.utils import classify_column

class Categorical_Table:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.columns = []
        self.stats = {}
        self.n = 0

        # Get the categorical variables/columns
        self.get_categoric_columns()

        # Fill in the table
        self.create_table()


    def get_categoric_columns(self):
        categoric_columns = []
        for column in self.df.columns:
            if classify_column(self.df[column]) != "num":
                categoric_columns.append(column)
        self.columns = categoric_columns
        self.n = len(categoric_columns)


    def create_table(self):
        for column in self.columns:
            self.get_stats(column)


    def get_stats(self, col):
        self.stats[col] = {}
        self.stats[col]["count"] = self.df[col].count()
        self.stats[col]["missing_count"] = self.df[col].isnull().sum()
        self.stats[col]["missing_percent"] = (self.df[col].isnull().sum() / len(self.df[col])) * 100
        self.stats[col]["categories"] = self.df[col].value_counts().to_dict()
        self.stats[col]["mode"] = self.df[col].mode()[0] if not self.df[col].mode().empty else np.nan
        self.stats[col]["mode_count"] = self.df[col].value_counts().iloc[0] if not self.df[col].value_counts().empty else np.nan
        self.stats[col]["mode_percent"] = (self.df[col].value_counts().iloc[0] / len(self.df[col])) * 100 if not self.df[col].value_counts().empty else np.nan
        self.stats[col]["second_mode"] = self.df[col].value_counts().index[1] if len(self.df[col].value_counts()) > 1 else np.nan
        self.stats[col]["second_mode_count"] = self.df[col].value_counts().iloc[1] if len(self.df[col].value_counts()) > 1 else np.nan
        self.stats[col]["second_mode_percent"] = (self.stats[col]["second_mode_count"] / len(self.df[col])) * 100 if len(self.df[col].value_counts()) > 1 else np.nan
        self.stats[col]["least_frequent_category"] = self.df[col].value_counts().index[-1] if len(self.df[col].value_counts()) > 0 else np.nan
        self.stats[col]["least_frequent_count"] = self.df[col].value_counts().iloc[-1] if len(self.df[col].value_counts()) > 0 else np.nan
        self.stats[col]["least_frequent_percent"] = (self.stats[col]["least_frequent_count"] / len(self.df[col])) * 100 if len(self.df[col].value_counts()) > 0 else np.nan
        self.stats[col]["entropy"] = -(self.df[col].value_counts(normalize=True) * np.log2(self.df[col].value_counts(normalize=True))).sum()
        self.stats[col]["normalized_entropy"] = self.stats[col]["entropy"] / np.log2(len(self.df[col].value_counts())) if len(self.df[col].value_counts()) > 1 else np.nan
        self.stats[col]["concentrated_ratio"] = self.stats[col]["mode_count"] / len(self.df[col]) if len(self.df[col]) > 0 else np.nan