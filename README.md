# Statistics-API

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


### Num vs Num:
1. Pearson's Correlation Coefficient (r)
2. Spearman's Rank-Order Coefficient (rho)
3. Distance Correlation
4. Kendall's Rank Correlation (tau?)
5. Coefficient of Detemrination (R^2)
6. Biserial / Point-Biserial Correlation
7. Nash-Sutcliffe Efficiency (NSE)


### Cat vs Cat:
1. Cramer's V
2. Cramer's Unbiased V
3. Goodman-Krushal's Lambda


### Num vs Cat:
1. Point-Biserial Correlation Coefficient


### Cat  vs Ord:
1. Rank-Biserial Correlation Coefficient


### Ord vs Ord and Ord vs Num
1. Spearman Rank Correlation
2. Kendall Rank Correlation Coefficient