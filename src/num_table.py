
import pandas as pd
import numpy as np
from src.stats.utils import classify_variable
from src.consts import numeric_table_columns

class Numerical_Table:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.columns = numeric_table_columns
        self.variables = []
        self.stats = {}
        self.n = 0

        # Get the numerical variables/columns
        self.get_numeric_variables()

        # Fill in the table
        self.create_table()


    def get_numeric_variables(self):
        numeric_variables = []
        for column in self.df.columns:
            if classify_variable(self.df[column]) == "num":
                numeric_variables.append(column)
        self.variables = numeric_variables
        self.n = len(numeric_variables)


    def create_table(self):
        for v in self.variables:
            self.get_stats(v)


    def get_stats(self, v):
        self.stats[v] = {}
        self.stats[v]["cnt"] = self.df[v].count()
        self.stats[v]["missing_cnt"] = self.df[v].isnull().sum()
        self.stats[v]["missing_pct"] = (self.df[v].isnull().sum() / len(self.df[v])) * 100
        self.stats[v]["outlier_cnt"] = ((self.df[v] < (self.df[v].quantile(0.25) - 1.5 * (self.df[v].quantile(0.75) - self.df[v].quantile(0.25)))) | (self.df[v] > (self.df[v].quantile(0.75) + 1.5 * (self.df[v].quantile(0.75) - self.df[v].quantile(0.25))))).sum()
        self.stats[v]["zeros_cnt"] = (self.df[v] == 0).sum()
        self.stats[v]["negative_cnt"] = (self.df[v] < 0).sum()
        self.stats[v]["unique_cnt"] = self.df[v].nunique()
        self.stats[v]["mean"] = self.df[v].mean()
        self.stats[v]["median"] = self.df[v].median()
        self.stats[v]["mode"] = self.df[v].mode()[0] if not self.df[v].mode().empty else np.nan
        self.stats[v]["std_dev"] = self.df[v].std()
        self.stats[v]["var"] = self.df[v].var()
        self.stats[v]["min"] = self.df[v].min()
        self.stats[v]["max"] = self.df[v].max()
        self.stats[v]["range"] = self.df[v].max() - self.df[v].min()
        self.stats[v]["p5"] = self.df[v].quantile(0.05)
        self.stats[v]["p10"] = self.df[v].quantile(0.10)
        self.stats[v]["p25"] = self.df[v].quantile(0.25)
        self.stats[v]["p75"] = self.df[v].quantile(0.75)
        self.stats[v]["p90"] = self.df[v].quantile(0.90)
        self.stats[v]["p95"] = self.df[v].quantile(0.95)
        self.stats[v]["iqr"] = self.df[v].quantile(0.75) - self.df[v].quantile(0.25)
        self.stats[v]["skew"] = self.df[v].skew()
        self.stats[v]["kurtosis"] = self.df[v].kurtosis()
        self.stats[v]["mad"] = self.df[v].sub(self.df[v].mean()).abs().mean()
        self.stats[v]["sem"] = self.df[v].sem()
        self.stats[v]["cv"] = (self.df[v].std() / self.df[v].mean()) * 100
        self.stats[v]["mean_ci_95_low"] = self.df[v].mean()-1.96*(self.df[v].std()/np.sqrt(len(self.df[v])))
        self.stats[v]["mean_ci_95_high"] = self.df[v].mean()+1.96*(self.df[v].std()/np.sqrt(len(self.df[v])))
