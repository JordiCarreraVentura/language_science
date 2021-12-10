# `pandas` manual

# Table of contents

1. [Loading data and performing basic `DataFrame` manipulations](#1-loading-data-and-performing-basic-dataframe-manipulations)
   1. Import data from a `csv` file
   2. Copy a dataset
   3. Load multiple files with glob and list comprehension
   4. Transform a `DataFrame` into a `dict`
   5. [Change column names](#1-D-change-column-names)
   6. Transpose a `DataFrame`
   7. Iterate over `DataFrame` rows
   8. Sort values in ascending order
   9. `inplace` _versus_ call
   10. Axes 0 and 1
2. Exploratory data analysis
   1. List information about a `DataFrame`
   2. List statistics about a `DataFrame`
   3. Get the first _n_ rows of a `DataFrame`
   4. Get the shape of a `DataFrame`
   5. Get the names of a `DataFrame`'s columns
   6. For categorical variables (i.e., not scalar) get the number of different values they take in the dataset
   7. For categorical variables again, get the set of unique values they can take
   8. For any variable (i.e. any given column of the `DataFrame`), get the set of unique values it can take and the occurrence count of each value on that column
3. Grouping
   1. Return a `DataFrame` object grouped by _species__ column
   2. Apply functions to groups
4. Subsetting
   1. By selecting columns
      1. by name (same as `df.loc`?)
      2. by number
   2. By dropping...
      1. ... columns
      2. ... rows
   3. By condition
      1. Rows containing exact matches of strings or integers
      2. Arbitrary conditions
5. Preprocessing
   1. Handling missing values
      1. Counting and assessing
      2. Filling
          1. Drop the rows or columns that contain them
          2. Replace/impute missing values
          3. Interpolate missing values
   2. Normalizing / Scaling values in a pandas column with sklearn
6. Element-wise calculations
   1. Running t-tests
7. SQL-style joining...
  1. ... by concatenating...
  2. or, given the following input data,
     1. by joining...
     2. ... by index joining...
     3. ... by joining on a key...
     4. ... or by merging on a key
8. Updating `DataFrame` values
  1. Transforming columns with `.apply` and *lambda* functions
  2. Changing a percentage string to a numerical value
  3. Encoding categorical variables
  4. Creating new columns


# 1. Loading data and performing basic `DataFrame` manipulations

### 1.A. Import data from a csv file

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
data = pd.read_csv("iris.csv")
```

### 1.B. Copy a dataset

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df = data.copy()
```

### 1.C. Load multiple files with glob and list comprehension

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

```
import glob
import pandas as pd
csv_files = glob.glob("path/to/folder/with/csvs/*.csv")
dfs = [pd.read_csv(filename) for filename in csv_files]
```

### 1.D. Transform a `DataFrame` into a `dict`

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

```
df_ = pd.DataFrame(dict(a=["a","b","c"], b=[1,2,3]))
df_dictionary = dict(zip(df_["a"], df_["b"]))
```

### 1.E. Change column names

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
_df = df.rename(columns={"species": "Species"})
_df.rename(columns={"Species": "species"}, inplace=True)
```

### 1.F. Transpose a `DataFrame`

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
_df = df.T
```

### 1.G. Iterate over `DataFrame` rows

[Source](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html)

```
# for row in df_.iterrows():
#     print(row)

# for row in df_.iteritems():
#     print(row)

for row in df_.itertuples():
    print(row)
```


### 1.H. Sort values in ascending order

[Source](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html)

```
df.sort_values(by = "sepal width (cm)", ascending=False)
```

### 1.I. `inplace` _versus_ call

Most methods leave the input `DataFrame` object unchanged and return a new one with the output of the method call. Therefore, using a standard Python variable assignment (`df = df.method()`) will be enough to store the output of the operation. However, in case we want to keep working with the same object, the keyword argument `inplace` must be added to the method call, which will prevent the method from returning a copy with the modified data and will apply the changes to the original one instead.

### 1.J. Axes 0 and 1

Axis 0 corresponds to rows (traverses the matrix vertically), all cells in a row.
Axis 1 corresponds to columns (traverses the matrix horizontally), all cells in a column.



















# 2. Exploratory data analysis

### 2.A. List information about a `DataFrame`

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
print(df.info())
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 150 entries, 0 to 149
Data columns (total 5 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   sepal length (cm)  150 non-null    float64
 1   sepal width (cm)   150 non-null    float64
 2   petal length (cm)  150 non-null    float64
 3   petal width (cm)   150 non-null    float64
 4   species            150 non-null    int64  
dtypes: float64(4), int64(1)
memory usage: 6.0 KB

```

### 2.B. List statistics about a `DataFrame`

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.describe()
```

```

       sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)     species
count         150.000000        150.000000         150.000000        150.000000  150.000000
mean            5.843333          3.057333           3.758000          1.199333    1.000000
std             0.828066          0.435866           1.765298          0.762238    0.819232
min             4.300000          2.000000           1.000000          0.100000    0.000000
25%             5.100000          2.800000           1.600000          0.300000    0.000000
50%             5.800000          3.000000           4.350000          1.300000    1.000000
75%             6.400000          3.300000           5.100000          1.800000    2.000000
max             7.900000          4.400000           6.900000          2.500000    2.000000

```


### 2.C. Get the first _n_ rows of a `DataFrame`

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.head()
```


### 2.D. Get the shape of a `DataFrame`

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.shape
```

### 2.E. Get the names of a `DataFrame`'s columns

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.columns
df.columns.tolist()
```

### 2.F. For categorical variables (i.e., not scalar) get the number of different values they take in the dataset

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df["species"].nunique()
```

### 2.G. For categorical variables again, get the set of unique values they can take

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df["species"].unique()
```

### 2.H. For any variable (i.e. any given column of the `DataFrame`), get the set of unique values it can take and the occurrence count of each value on that column

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df["species"].value_counts()
```





# 3. Grouping

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

> The key function for this task is groupby() and is mainly used
> for aggregating rows based on categorical features.

### 3.A. Return a `DataFrame` object grouped by "species" column


[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.groupby("species")
```

### 3.B. Apply functions to groups

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df["sepal length (cm)"].groupby(df["species"]).mean()
print(df.groupby("species").agg([np.sum, np.mean, np.std]))
```

`DataFrame.agg` performs an aggregation but in a UX sense of aggregation, not a computational sense: the functions specified as the argument for `agg` are already performed element-wise over the whole columns of the DataFrame, so no further aggregation is required and an "aggregated" value is already produced. The aggregation that the method `agg` refers to is the fact that a single summary table will be returned that displays all the functions specified as the argument of `agg` as separate rows.

Some more examples:

```
df_ = pd.DataFrame([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9],
                   [np.nan, np.nan, np.nan]],
                  columns=['A', 'B', 'C'])

df_.agg(['sum', 'min'])

#         A     B     C
# sum  12.0  15.0  18.0
# min   1.0   2.0   3.0

df_.agg({'A' : ['sum', 'min'], 'B' : ['min', 'max']})

#         A    B
# sum  12.0  NaN
# min   1.0  2.0
# max   NaN  8.0
```



#  4. Subsetting

### 4.A. By selecting columns

#### 4.A.a. by name (same as `df.loc`?)

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df["sepal length (cm)"]
df[["sepal length (cm)", "sepal width (cm)", "petal length (cm)"]]
```

#### 4.A.b. by number

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.iloc[:, 2:4]         # columns 2 and 3 of all rows
df.iloc[3:10,]          # all columns of rows 3 to 10
df.iloc[:, [1,3,4]]     # columns 1, 3 and 4 of all rows
```


### 4.B. By dropping...

#### 4.B.a. ... columns

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.drop("sepal length (cm)", axis=1)
```

#### 4.B.b. ... rows

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.drop(df.index[1]) # 1 is row index to be deleted
```

### 4.C. By condition

#### 4.C.a. Rows containing exact matches of strings or integers

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df[df["species"].isin([0, "setosa"])]
```

#### 4.C.b. Arbitrary conditions

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df[df['sepal length (cm)'] >= 5]

df.query('species == 0').shape)


df[
    (df['sepal length (cm)'] > 2)
    & (df['sepal length (cm)'] < 4)
]

df[
    (df['sepal length (cm)'] > 2)
    | (df['sepal length (cm)'] < 2)
]

df[
    (df['sepal length (cm)'] > 2)
    & (df['sepal length (cm)'] > 5)
]

df[
    ((df['sepal length (cm)'] > 2)
    & (df['sepal length (cm)'] > 5))
    | (df['sepal length (cm)'] > 3)
]

```

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)


```
from test_data import warlords_data

NULL = np.NaN
df_ = pd.DataFrame(warlords_data)
import numpy as np
df_.replace({'Special': {None: NULL}}, inplace=True)

# human units with strength greater than 3
query = (df_["Race"] == 'Human') & (df_["Strength"] > 3)
df_[query]

# human units with strength greater than 3 AND special abilities
query = (df_["Race"] == 'Human') & (df_["Strength"] > 3) & (pd.notnull(df_['Special']))
df_[query]

# human units with strength greater than 3 AND Upkeep equal to 7
query = (df_["Race"] == 'Human') & (df_["Strength"] > 3) & (df_['Upkeep'] == 7)
df_[query]

# human units with strength greater than 3 and terrain bonus in plains
query = (df_["Race"] == 'Human') & (df_["Strength"] > 3) & (df_['Terrain bonus'].str.contains('Plains'))
df_[query]

# human units with movement greater than 25 or special abilities
query = (df_["Race"] == 'Human') & ((df_["Movement"] > 25) | (pd.notnull(df_['Special'])))
df_[query]

# units with movement greater than 25 or special abilities
query = (df_["Movement"] > 25) | (pd.notnull(df_['Special']))
df_[query]

```





# 5. Preprocessing

### 5.A. Handling missing values

In case our dataset does not have missing values and we need to create fake ones, we can use the following code:

```
column_names = df.columns
n_rows, n_columns = df.shape
random.seed(88)
for _ in range(10):
    col_idx = random.randrange(len(column_names))
    column_name = column_names[col_idx]
    row_idx = random.randrange(n_rows)
    df.at[row_idx, column_name]= None
```

### 5.A.a. Counting and assessing

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.isnull().sum()
df.isnull().sum() / float(len(df))) * 100
```

### 5.A.b. Filling

### 5.A.b.i. Drop the rows or columns that contain them

*Drop rows*

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.dropna(inplace=True)
```

*Drop columns*

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
_df.dropna(axis=1, inplace=True)
```

### 5.A.b.ii. Replace/impute missing values

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df.fillna(-9999, inplace=True)
df.fillna(np.NaN, inplace=True)
df.fillna("data missing", inplace=True)
df.fillna(df.mean(), inplace=True)
```

*Replace `na` values of specific columns with mean value*

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
_df = df[:].copy()
before = _df.shape
for column in df.columns:
    if isinstance(_df[column][0], str):
        continue
    _df[column].fillna(df[column].mean(), inplace=True)
```

### 5.A.b.iii. Interpolate missing values

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

(With time-series data)

```
df.interpolate()                        # whole dataframe
df["sepal length (cm)"].interpolate()   # specific column
```


### 5.B. Normalizing / Scaling values in a pandas column with sklearn

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

```
df = pd.DataFrame(dict(a=["a","b","c"], b=[1,2,3]))
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['b'] = scaler.fit_transform(df_["b"].values.reshape(-1,1))
```




# 6. Element-wise calculations

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)


```
df[["sepal length (cm)", "sepal width (cm)"]].mean()
df[["sepal length (cm)", "sepal width (cm)"]].agg([np.sum, np.mean])
```

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)


# 6.1. Running t-tests

```
from scipy.stats import ttest_rel

data = np.arange(0,1000,1)
data_plus_noise = np.arange(0,1000,1) + np.random.normal(0,1,1000)
df = pd.DataFrame(dict(data=data, data_plus_noise=data_plus_noise))

# expected output:
# Ttest_relResult(statistic=-1.2717454718006775, pvalue=0.20375954602300195)

```



# 7. SQL-style joining...

### 7.A. ... by concatenating...

[Source](https://towardsdatascience.com/a-checklist-for-data-wrangling-8f106c093fef)

```
df1 = df[["sepal length (cm)", "petal length (cm)"]]
df2 = df[["sepal length (cm)", "petal length (cm)"]]

# adds df2's columns to the left of df1's
dfx = pd.concat([df1, df2], axis = 1)   
```

### 7.B. or, given the following input data,

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)


```
df = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3', 'K4', 'K5'],
                   'A': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']})


other = pd.DataFrame({'key': ['K0', 'K1', 'K2'],
                      'B': ['B0', 'B1', 'B2']})

```


### 7.B.a. by joining...

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)


```
_df = df.join(other, lsuffix='_caller', rsuffix='_other')
```

### 7.B.b. ... by index joining...

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)


```
_df = df.set_index('key').join(other.set_index('key'))
```

### 7.B.c. ... by joining on a key...

This is the best option, the output shape is more logical

```
_df = df.join(other.set_index('key'), on='key')     
```

### 7.B.d. ... or by merging on a key

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

This is also good, just as good as the previous option

```
df1 = pd.DataFrame(dict(a=[1,2,3], b=[10,20,30], col_to_merge=["a","b","c"]))
df2 = pd.DataFrame(dict(d=[100,20,10], col_to_merge=["b","c","a"]))
df_merged = df1.merge(df2, on='col_to_merge')
```



# 8. Updating `DataFrame` values

### 8.A. Transforming columns with `.apply` and *lambda* functions

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

```
class Square:

    def __init__(self):
        return

    def __call__(self, x):
        return x ** 2


df = pd.DataFrame(dict(a=[10,20,30,40,50]))

square = lambda x: x ** 2

df["b"]=df["a"].apply(square)

df["c"]=df["a"].apply(Square())

```


### 8.B. Changing a percentage string to a numerical value

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

```
def change_to_numerical(x):
    try:
        x = int(x.strip("%")[:2]) / 100.0
    except:
        x = int(x.strip("%")[:1]) / 100.0
    return x

df = pd.DataFrame(dict(a=["A","B","C"],col_with_percentage=["10%","70%","20%"]))
df["col_with_percentage"] = df["col_with_percentage"].apply(change_to_numerical)
```


### 8.C. Encoding categorical variables

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

In the same way as `sklearn.processing.LabelEncoder` but directly in pandas.

```
_df = df.replace(
    {"species":
        {
            0: "setosa",
            1: "versicolor",
            2: "virginica"
        }
    }
)
```


### 8.D. Creating new columns

[Source](https://www.kdnuggets.com/2021/08/15-python-snippets-optimize-data-science-pipeline.html)

Often big part of feature engineering.

```
df['2x sepal length'] = df["sepal length (cm)"] * 2
df['sepal width < 3'] = ["short" if i < 3 else "long" for i in df["sepal width (cm)"]] 
```





