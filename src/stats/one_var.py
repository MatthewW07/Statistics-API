""" Functions to calculate given statistics for a single variable """

"""
ALL functions:
1. Count
2. Missing Count
3. Missing Percent
4. Outlier Count
5. Unique Count
6. Zeros Count
7. Negative Count
8. Mean
9. Mode
10. Standard Deviation (std_dev)
11. Variance (var)
12. Range
13. Minimum (min)
14. 5th Percentile (p5)
15. 10th Percentile (p10)
16. 25th Percentile (p25)
17. Median
18. 75th Percentile (p75)
19. 90th Percentile (p90)
20. 95th Percentile (p95)
21. Maximum (max)
22. Inter-Quartile Range (iqr)
23. Skewness (skew)
24. Kurtosis
25. Mean Absolute Deviation (mad)
26. Standard Error of the Mean (sem)
27. Coefficient of Variation
28. Mean 95% Confidence Interval Lower Bound (mean_ci_95_low)
29. Mean 95% Confidence Interval Upper Bound (mean_ci_95_high)
"""

def numeric_stats(df, v, statistic):
    match statistic:
        case "count": df[v].count()

"""
self.stats[v]["count"] = self.df[v].count()
self.stats[v]["missing_count"] = self.df[v].isnull().sum()
self.stats[v]["missing_percent"] = (self.df[v].isnull().sum() / len(self.df[v])) * 100
self.stats[v]["outlier_count"] = ((self.df[v] < (self.df[v].quantile(0.25) - 1.5 * (self.df[v].quantile(0.75) - self.df[v].quantile(0.25)))) | (self.df[v] > (self.df[v].quantile(0.75) + 1.5 * (self.df[v].quantile(0.75) - self.df[v].quantile(0.25))))).sum()
self.stats[v]["zeros_count"] = (self.df[v] == 0).sum()
self.stats[v]["negative_count"] = (self.df[v] < 0).sum()
self.stats[v]["unique_count"] = self.df[v].nunique()
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
"""