
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
        self.get_numeric_columns()

        # Fill in the table
        self.create_table()


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


    def get_stats(self, col):
        self.stats[col] = {}
        self.stats[col]["count"] = self.df[col].count()
        self.stats[col]["missing_count"] = self.df[col].isnull().sum()
        self.stats[col]["missing_percent"] = (self.df[col].isnull().sum() / len(self.df[col])) * 100
        self.stats[col]["outlier_count"] = ((self.df[col] < (self.df[col].quantile(0.25) - 1.5 * (self.df[col].quantile(0.75) - self.df[col].quantile(0.25)))) | (self.df[col] > (self.df[col].quantile(0.75) + 1.5 * (self.df[col].quantile(0.75) - self.df[col].quantile(0.25))))).sum()
        self.stats[col]["zeros_count"] = (self.df[col] == 0).sum()
        self.stats[col]["negative_count"] = (self.df[col] < 0).sum()
        self.stats[col]["unique_count"] = self.df[col].nunique()
        self.stats[col]["mean"] = self.df[col].mean()
        self.stats[col]["median"] = self.df[col].median()
        self.stats[col]["mode"] = self.df[col].mode()[0] if not self.df[col].mode().empty else np.nan
        self.stats[col]["std_dev"] = self.df[col].std()
        self.stats[col]["var"] = self.df[col].var()
        self.stats[col]["min"] = self.df[col].min()
        self.stats[col]["max"] = self.df[col].max()
        self.stats[col]["range"] = self.df[col].max() - self.df[col].min()
        self.stats[col]["p5"] = self.df[col].quantile(0.05)
        self.stats[col]["p10"] = self.df[col].quantile(0.10)
        self.stats[col]["p25"] = self.df[col].quantile(0.25)
        self.stats[col]["p75"] = self.df[col].quantile(0.75)
        self.stats[col]["p90"] = self.df[col].quantile(0.90)
        self.stats[col]["p95"] = self.df[col].quantile(0.95)
        self.stats[col]["iqr"] = self.df[col].quantile(0.75) - self.df[col].quantile(0.25)
        self.stats[col]["skew"] = self.df[col].skew()
        self.stats[col]["kurtosis"] = self.df[col].kurtosis()
        self.stats[col]["mad"] = self.df[col].sub(self.df[col].mean()).abs().mean()
        self.stats[col]["sem"] = self.df[col].sem()
        self.stats[col]["cv"] = (self.df[col].std() / self.df[col].mean()) * 100
        self.stats[col]["mean_ci_95_low"] = self.df[col].mean()-1.96*(self.df[col].std()/np.sqrt(len(self.df[col])))
        self.stats[col]["mean_ci_95_high"] = self.df[col].mean()+1.96*(self.df[col].std()/np.sqrt(len(self.df[col])))
