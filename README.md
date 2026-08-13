
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

## The API

Here you will learn how to use the codebase. First, make sure you have a `.csv` file ready. 

Once I learn how it works, I'll document it here.

## Local Setup

1. Clone the API
`git clone https://github.com/Matthew07/Statistics-API` and `cd Statistics-API`
2. Make virtual environment:
`python -m venv venv` or `uv venv`
3. Install dependencies
`pip install -r requirements.txt` or `uv pip install -r requirements.txt`
4. Start server
`uvicorn main:app`


# The Heatmap


# The Numerical Table


# The Categorical Table



*** 

## Statistics-API

BIG IDEA: i should change this all to Rust. it's for the learning. and cause it takes FOREVER to do a 20 x 20 map

last stats project was mid cause didn't know how to do anything and ai-ed a bunch of it

this one will try to improve it except without stupid frontend stuff

jk once the api stuff is good i'll have ai make a good frontend like last time

this one will also be public from creation


## Planning

k so basically need make it good with classes and stuff

### Heatmap
- make heatmap a class
    1. importantly will have n x n matrix
    2. maybe some metadata like columns
- make each cell a class
    1. have variable x
    2. have variable y
    3. have classification of x
    4. have classifictaion of y
    5. have list of correlations (like eta, r, rho, p, cramers, some other guy i forgot, etc.)
    6. have graph object 
- need graph object???
    1. have list of plots
    2. have dictionary of plot_name -> the graph (i think plotly makes graphs as objects so ye)
- NOTE: there can be multiple graphs for one cell (violin, box, density, scatter, etc)


### Numerical Table
- make table for numerical data as a class
    1. store count of numerical variables
    2. list (in order) of what descriptive stats are included
    3. store each row as a dictionary (variable: str -> row: list)
- NOTE: goal stats are: count, mean, variance, std dev, range, min, 10th, 25th, median, 75th, 90th, max, skew, kurt


### Categorical Table
- make table for categorical data as a class
    1. store count of categorical variables
    2. list (in order) of what descriptive stats are included
    3. store each row as a dictionary (variable: str -> row: list)
- NOTE: goal stats are: 
- NOTE: categorical data is harder, cause its good to have like a CATEGORY <-> FREQUENCY stuff
- idk what to do still


### 2 Variable Stats stuff
- make some functions to really analyze 2 variable comparisons
- this stuff will prob be used for the heatmap, so GOTTA MAKE IT GOOD
    1. comparison functions(x, y): returns dictionary of comparison -> value
    2. make graph(x, y, type=None): returns graph of specified type (or of default type)
    3. determine variables(x, y): take two variables and return what type it is (cat vs. cat, num vs cat, etc.)



## Comparison Data
need to research these to see what exactly they compare
also need to figure out how to classify numerical vs categorical vs ordinal data
tbh i can prob start by just keeping numbers as numbers, but i should add ordinal stuff later
like maybe there'll be an option to treat a numerical variable as ordinal
actually that's an interface thing; all i need to do here is use default parameters that can be changed
also what is there for data types?

- Numerical:
    1. discrete
    2. continuous
    3. categorical
- Categorical:
    1. Multiple
        1. Ordinal
        2. Non-ordinal
    2. Binary 
        1. Ordinal
        2. Non-ordinal


### Num vs Num:
1. Pearson's Correlation Coefficient (r)
2. Spearman's Rank-Order Coefficient (rho)
3. Distance Correlation
4. Kendall's Rank Correlation (tau?)
5. Coefficient of Detemrination (R^2)
6. Nash-Sutcliffe Efficiency (NSE)


### Cat vs Cat:
1. Cramer's V
2. Cramer's Unbiased V
3. Goodman-Krushal's Lambda


### Num vs Cat:
1. Eta Coefficient


### Num vs Bin:
1. Biserial / Point-Biserial Correlation Coefficient



### stuff to look into:

Nominal apparently:
- The Percent Maximum Difference[8]
- The phi coefficient
- Tschuprow's T
- The uncertainty coefficient
- The Lambda coefficient
- The Rand index
- Davies–Bouldin index
- Dunn index
- Jaccard index
- Fowlkes–Mallows index