
***
# Statistics API Project (The New Version)
***

# Introduction

This codebase is a project I did to try to accomplish the following things:

1. Learn some new statistics formulas / coefficients / metrics.
2. Get a feel to using Pandas and Numpy.
3. Making a full, working, and clean API.

Now, what does the project do, you may ask. It's quite simple. Given some `.csv` file with columns of data, it returns **three** different things:

1. A **Heatmap** showing correlation coefficients. between all pairs of data. However, the correlation coefficients in the Heatmap are not just Pearson's Correlation Coefficient that everyone learns, but rather a variety of different metrics. After all, there will often be *categorical* and *numerical* data that have to be compared, and the *categorical* data may be *binary*, *nominal*, *ordinal*, etc. Lots of choices.

2. A **Numerical Data Table** that shows important metrics for *all numerical variables/columns*. These metrics include (but are not limited to) *mean*, *min*, *max*, *range*, *25th percentile*, *75th percentile*, *skewness*, and hopefully some more.

3. A **Categorical Data Table* that shows important metrics/descriptions for *all categorical variables/columns* (except any columns for labelling...). These descriptions include (but are not limited to) *type of categorical data*, *number of categories*, *some other stuff...*, yeah. There will likely be some fancy metrics that go here.

4. Eventually, I wish to add a way to directly compare two variables/columns to determine *all comparisons/metrics*.

MAYBE, if I have time, I'll add a way to directly compare two variables to get more comparisons between them.

***
# Usage

## Local Setup

1. Clone the API
`git clone https://github.com/Matthew07/Statistics-API` and `cd Statistics-API`
2. Make virtual environment:
`python -m venv venv` or `uv venv`
3. Install dependencies
`pip install -r requirements.txt` or `uv pip install -r requirements.txt`
4. Start server
`uvicorn main:app`

## The Heatmap

This is the main tool of the repository. It compute statistics for every possible pair of two variables from a given dataset. Here is the current list of statistics and when they are computed:

- **Numeric vs Numeric**:
    1. Pearson's Correlation Coefficient (r)
    2. Spearman's Rank-Order Coefficient (rho)
    3. Distance Correlation
    4. Kendall's Rank Correlation (tau?)
    5. Coefficient of Detemrination (R^2)
    6. Nash-Sutcliffe Efficiency (NSE)

- **Categoric vs Categoric**:
    1. Cramer's V
    2. Cramer's Unbiased V
    3. Goodman-Krushal's Lambda

- **Numeric vs Categoric**:
    1. Eta Coefficient
    2. Biserial
    3. Point-Biserial Correlation Coefficient

## The Numerical Table

In the **Numerical Table**, the following statistics will be computed for every *numerical variable/column*:

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

## The Categorical Table

In the **Categorical Table**, the following statistics will be computed for every *numerical variable/column*:

1. Count
2. Missing Count
3. Missing Percent
4. Categories
5. Mode
6. Mode Count
7. Mode Percent
8. Second Mode
9. Second Mode Count
10. Second Mode Percent
11. Least Frequent Category
12. Least Frequent Count
13. Least Frequent Percent
14. Entropy
15. Normalized Entropy
16. Concentration Ratio

## Visualization

This project also includes an actual webpage to use the tools outside the terminal. No graphs are included, but you can see the heatmap the tables and look through some values.

***
# Future Improvements

Here are some ways this project could be improved

## More Statistics

There are way more statistics / metrics / indices / whatever out there that could be included here. Here's a small list of possible things to look at:

1. The Percent Maximum Difference
2. The phi coefficient
3. Tschuprow's T
4. The Uncertainty Coefficient
5. The Lambda Coefficient
6. The Rand Index
7. Davies–Bouldin Index
8. Dunn Index
9. Jaccard Index
10. Fowlkes–Mallows Index

## More Depth for Categorical Data

There are many types of categorical data. Certain statistics thrive off of specific categorical types but not others. For example, choosing whether or not to use Cramer's V *Biased* or *Unbiased* depends on whether the categorical data is *Binary* or *Multiclass*. Here's a small tree diagram that could be expanded upon:

Categorical
    1. Multiclass
        1. Ordinal
        2. Non-Ordinal
    2. Binary
        1. Ordinal
        2. Non-Ordinal

Ideally, the *classify_variable()* function (found at `src/stats/utils.py`) could be improved to specify which type of `cat` (categorical) data a variable is, and in turn the default values (in the *Heatmap* or choosing between *biased/unbiased*) would be changed.

## Further Visualizations

Graphs were not included in this project because I wanted to keep it light. However, if needed, perhaps certain plots could be included. Maybe in the *Heatmap*, if a cell is selected, the frontend would show a graphs option. There are more ways to do this. Here's a list of possible graphs to include:

- One-variable: **Violin**, **Box**, **Density**
- Two-variable: **Scatterplot**, etc.

***
# The End
