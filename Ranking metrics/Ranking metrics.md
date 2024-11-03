# Ranking metrics

1. [Online metrics](#online-metrics)
   1. [Hit Ratio](#hit-ratio)
2. [Offline metrics](#offline-metrics)
   1. [Reciprocal Rank and Mean Reciprocal Rank](#reciprocal-rank-and-mean-reciprocal-rank)
   2. [Mean Average Precision](#mean-average-precision-map)
3. [Examples](#examples)
4. [References](#references)

## Online metrics

### Hit Ratio

[Source 1](#reference_1)

> the fraction of users for which the correct answer is included in the recommendation list of length $L$.

$D = \text{the superset containing every set of recommendations }d\text{ served to a user, such that }|d| = L$

$y = \text{the correct answer}$

$$HR_L = \frac{|d: d \in D \land y \in d|}{|D|}$$

**NOTE**: $L$ is a parameter.

## Offline metrics

### Reciprocal Rank and Mean Reciprocal Rank

[Source 1](#reference_1), [Back to top](#ranking-metrics)

$D = \text{the superset containing every ranked set of recommendations }d\text{ served to a user, such that }|d| = L$

$$RR(d) = \sum\limits_{i: 1 ≤ i ≤ L} \frac{relevance_i}{rank_i}$$

$$MRR(D) = \frac{ \sum\limits_{i = 1}^{|D|} RR(D_i) }{|D|} $$

**NOTE**: _one could argue that hit ratio is actually a special case of MRR in which RR(d) is binary, as it becomes 1 if there is a relevant item in the list, 0 otherwise._

### Mean Average Precision (MAP)

[Source 1](#reference_1), [Back to top](#ranking-metrics)

$K = \text{the maximum number of top elements we want to consider}$

$k = \text{the number of top elements we want to consider to calculate metrics such that } 1 ≤ k ≤ K$

$D = \text{the superset containing every ranked list of recommendations }d\text{ served to a user, such that }|d| = k$

$$AP(D_i) = \sum\limits_{k = 1}^{K} \text{Precision@}k(D_i) \times RelevanceMask_i$$

$$MAP(D) = \frac{\sum\limits_{i = 1}^{|D|} AP(D_i)}{|D|}$$

### Normalized Discounted Cumulative Gain

[Source](https://towardsdatascience.com/normalized-discounted-cumulative-gain-ndcg-the-ultimate-ranking-metric-437b03529f75), [Back to top](#ranking-metrics)

#### Cumulative Gain (CG)

> The **.cumulative gain** is the sum of the relevance scores of items in the list.

$$CG = \sum\limits_{i = 1}^{K} \text{relevance}(K_i)$$

> If you’re computing NDCG@10, CG@10 will be 12 for both lists.
> 
> If you’re computing NDCG@5, CG@5 for Model A is 7, and for Model B is 10

#### Discount Factor (DF)

> The **discount factor** involves using a logarithmic discounting factor to perform a weighted sum of the relevance scores of items in the list. The discounting factor is weighted based on the item’s position in the list.

It is based on the same intuition as the reciprocal rank but it is smoothed by the use of the logarithm: for the item in the 10th rank, instead of computing the score as $1 / 10$ (the reciprocal rank), we calculate it as $1 / log(10)$, which means that the denominator is smaller and the result, therfore, higher. So, while we still penalize higher ranks, we are not penalizing them as much as the reciprocal rank, probably reflecting the intuition that _there is not a single correct answer_, as well as smoothing out/squeezing together potential anomalies in the scoring function.

$$DF = \frac{1}{log_2(1 + i)}$$


#### Normalization constant

> We want to normalize the model’s DCG by dividing it by the DCG obtained by an ideal ranker.
> 
> An ideal ranks the items in descending order of relevance scores.


#### Normalized Discounted Cumulative Gain

$\text{Candidate Discounted Cumulative Gain} = \text{DCG over relevance scores calculated after sorting by either model's score, and selecting the top }k$

$$DCG_k = \sum\limits_{i = 1}^{k} \frac{relevance(Y_i)}{log_2 (1 + i)}$$

$\text{Ideal Discounted Cumulative Gain} = \text{DCG calculated after sorting by relevance instead of either model's score}$

$$DCG_k = \sum\limits_{i = 1}^{k} \frac{relevance_i}{log_2 (1 + i)}$$

$$NDCG = \frac{\text{Candidate Discounted Cumulative Gain}}{\text{Ideal Discounted Cumulative Gain}}$$

# Examples

[Back to top](#ranking-metrics)

### MAP @ k


```python
import random
movies = list(range(10))
n_users = 10
n_relevant = 5

get_preferences = lambda x: random.sample(movies, len(movies))

movie_preferences = [
    get_preferences(u)
    for u in range(n_users)
]

relevance_masks = []
for mvps in movie_preferences:
    relevance_mask = dict([])
    for idx, mvp in enumerate(mvps):
        if idx < n_relevant:
            relevance_mask[mvp] = 1
        else:
            relevance_mask[mvp] = 0
    relevance_masks.append(relevance_mask)

accuracy = 0.8
movie_recommendations = [
    preferences if random.random() < accuracy
    else random.sample(preferences, len(preferences))
    for preferences in movie_preferences
]

for rm, mv, mr in zip(relevance_masks, movie_preferences, movie_recommendations):
    print(mv)
    print(mr)
    print(rm)
    print()
```

    [1, 4, 6, 9, 8, 2, 0, 3, 7, 5]
    [1, 4, 6, 9, 8, 2, 0, 3, 7, 5]
    {1: 1, 4: 1, 6: 1, 9: 1, 8: 1, 2: 0, 0: 0, 3: 0, 7: 0, 5: 0}
    
    [9, 6, 8, 4, 5, 1, 7, 3, 0, 2]
    [9, 6, 8, 4, 5, 1, 7, 3, 0, 2]
    {9: 1, 6: 1, 8: 1, 4: 1, 5: 1, 1: 0, 7: 0, 3: 0, 0: 0, 2: 0}
    
    [1, 0, 7, 6, 8, 9, 5, 4, 3, 2]
    [1, 0, 7, 6, 8, 9, 5, 4, 3, 2]
    {1: 1, 0: 1, 7: 1, 6: 1, 8: 1, 9: 0, 5: 0, 4: 0, 3: 0, 2: 0}
    
    [9, 4, 6, 2, 0, 3, 7, 1, 5, 8]
    [9, 4, 6, 2, 0, 3, 7, 1, 5, 8]
    {9: 1, 4: 1, 6: 1, 2: 1, 0: 1, 3: 0, 7: 0, 1: 0, 5: 0, 8: 0}
    
    [8, 9, 5, 3, 6, 2, 4, 0, 1, 7]
    [7, 3, 9, 5, 8, 6, 2, 4, 0, 1]
    {8: 1, 9: 1, 5: 1, 3: 1, 6: 1, 2: 0, 4: 0, 0: 0, 1: 0, 7: 0}
    
    [6, 4, 5, 0, 9, 1, 7, 2, 3, 8]
    [6, 4, 5, 0, 9, 1, 7, 2, 3, 8]
    {6: 1, 4: 1, 5: 1, 0: 1, 9: 1, 1: 0, 7: 0, 2: 0, 3: 0, 8: 0}
    
    [3, 9, 7, 6, 1, 5, 0, 8, 4, 2]
    [3, 9, 7, 6, 1, 5, 0, 8, 4, 2]
    {3: 1, 9: 1, 7: 1, 6: 1, 1: 1, 5: 0, 0: 0, 8: 0, 4: 0, 2: 0}
    
    [7, 4, 2, 5, 3, 0, 8, 6, 1, 9]
    [7, 4, 2, 5, 3, 0, 8, 6, 1, 9]
    {7: 1, 4: 1, 2: 1, 5: 1, 3: 1, 0: 0, 8: 0, 6: 0, 1: 0, 9: 0}
    
    [2, 9, 4, 0, 6, 7, 8, 5, 1, 3]
    [5, 2, 0, 1, 8, 9, 3, 6, 4, 7]
    {2: 1, 9: 1, 4: 1, 0: 1, 6: 1, 7: 0, 8: 0, 5: 0, 1: 0, 3: 0}
    
    [1, 5, 8, 3, 4, 0, 9, 2, 7, 6]
    [1, 5, 8, 3, 4, 0, 9, 2, 7, 6]
    {1: 1, 5: 1, 8: 1, 3: 1, 4: 1, 0: 0, 9: 0, 2: 0, 7: 0, 6: 0}
    



```python
def metric_at_k(denom, y_true, y_pred, k=2, relevance_masks=[], rounding=4):
    tp = 0
    p = 0
    t = 0
    if relevance_masks:
        for preferences, recommendations, relevance_mask in zip(y_true, y_pred, relevance_masks):
            expected = {mv for mv in preferences[:k] if relevance_mask[mv]}
            predicted = {mv for mv in recommendations[:k] if relevance_mask[mv]}
            true_positives = expected.intersection(predicted)
            tp += len(true_positives)
            p += k
            t += sum(relevance_mask.values())
    else:
        for preferences, recommendations in zip(y_true, y_pred):
            expected = {mv for mv in preferences[:k]}
            predicted = {mv for mv in recommendations[:k]}
            true_positives = expected.intersection(predicted)
            tp += len(true_positives)
            p += k
            t += len(expected)
    return round(tp / p if denom == 'precision' else tp / t, rounding)

def precision_at_k(y_true, y_pred, k=2, relevance_masks=[], rounding=4):
   return metric_at_k('precision', y_true, y_pred, k=k, relevance_masks=relevance_masks, rounding=rounding)

def recall_at_k(y_true, y_pred, k=2, relevance_masks=[], rounding=4):
   return metric_at_k('recall', y_true, y_pred, k=k, relevance_masks=relevance_masks, rounding=rounding)

```


```python
print(precision_at_k(movie_preferences, movie_recommendations, 4))
print(recall_at_k(movie_preferences, movie_recommendations, 4))
print(recall_at_k(movie_preferences, movie_recommendations, 4, relevance_masks))
```

    0.925
    0.925
    0.74


#### Normalized Discounted Cumulative Gain


```python
from math import log
import random
from typing import Iterable, Union

import pandas as pd
```


```python
def normalized_discounted_cumulative_gain(df: pd.DataFrame, column_name: str, k: int) -> float:
    if not isinstance(df, pd.DataFrame):
        raise TypeError(type(df), pd.DataFrame)
    if not k:
        k = df.shape[0]

    # --- dcg ---
    _df = df.sort_values(column_name, ascending=True if column_name != "relevance" else False).head(k)
    _df.discount_factor = [1 / log(1 + idx + 1) for idx in range(_df.shape[0])]
    dcg = (_df.relevance / df.discount_factor).sum()

    # --- idcg ---
    df.sort_values("relevance", ascending=False)
    df.discount_factor = [1 / log(1 + idx + 1) for idx in range(df.shape[0])]
    idcg = (df.head(k).relevance / df.head(k).discount_factor).sum()
    
    return dcg / idcg
```


```python
relevance_by_action = {
    "Viewed": 0,
    "Clicked": 1,
    "Shared": 2,
    "AddedToCart": 3,
    "Ordered": 4,
}

actions = list(relevance_by_action.keys())
item_ids = list(range(10))

event_items = [random.choice(item_ids) for _ in range(100)]
event_actions = [random.choice(actions) for _ in event_items]

events = []
for item, action in zip(event_items, event_actions):
    event = (
        item,
        action,
        relevance_by_action[action],
        round(((5 / (relevance_by_action[action] + 1)) / 10) if random.random() >= 0.2 else random.uniform(0, 1.0), 2),
        round(random.uniform(0, 1.0), 2)
    )
    events.append(event)

df = pd.DataFrame(events, columns=["item", "action", "relevance", "model_a", "model_b"])
df["discount_factor"] = discount_factor(df.sort_values("relevance").relevance)

df_model_a = df.copy().drop("model_b", axis=1).sort_values("model_a", ascending=True)
df_model_b = df.copy().drop("model_a", axis=1).sort_values("model_b", ascending=True)
df_ideal = df.copy().drop(["model_a", "model_b"], axis=1).sort_values("relevance", ascending=False)
```


```python
df_model_a.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>item</th>
      <th>action</th>
      <th>relevance</th>
      <th>model_a</th>
      <th>discount_factor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20</th>
      <td>5</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.1</td>
      <td>0.323515</td>
    </tr>
    <tr>
      <th>46</th>
      <td>7</td>
      <td>AddedToCart</td>
      <td>3</td>
      <td>0.1</td>
      <td>0.258318</td>
    </tr>
    <tr>
      <th>47</th>
      <td>6</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.1</td>
      <td>0.256949</td>
    </tr>
    <tr>
      <th>32</th>
      <td>5</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.1</td>
      <td>0.283578</td>
    </tr>
    <tr>
      <th>50</th>
      <td>9</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.1</td>
      <td>0.253085</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_model_b.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>item</th>
      <th>action</th>
      <th>relevance</th>
      <th>model_b</th>
      <th>discount_factor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>21</th>
      <td>7</td>
      <td>Clicked</td>
      <td>1</td>
      <td>0.01</td>
      <td>0.318929</td>
    </tr>
    <tr>
      <th>77</th>
      <td>2</td>
      <td>Shared</td>
      <td>2</td>
      <td>0.03</td>
      <td>0.228862</td>
    </tr>
    <tr>
      <th>69</th>
      <td>8</td>
      <td>AddedToCart</td>
      <td>3</td>
      <td>0.03</td>
      <td>0.234594</td>
    </tr>
    <tr>
      <th>26</th>
      <td>3</td>
      <td>AddedToCart</td>
      <td>3</td>
      <td>0.05</td>
      <td>0.300102</td>
    </tr>
    <tr>
      <th>24</th>
      <td>8</td>
      <td>Viewed</td>
      <td>0</td>
      <td>0.05</td>
      <td>0.306928</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(
    normalized_discounted_cumulative_gain(df, "model_a", 10000),
    normalized_discounted_cumulative_gain(df, "model_b", 10000),
    normalized_discounted_cumulative_gain(df, "relevance", 10000)
)
print(
    normalized_discounted_cumulative_gain(df, "model_a", 10),
    normalized_discounted_cumulative_gain(df, "model_b", 10),
    normalized_discounted_cumulative_gain(df, "relevance", 10)
)
```

    1.0 1.0 1.0
    3.707535015463046 2.488451270660452 3.9773980299904035



```python
df_ideal["factor"] = discount_factor(df_ideal["item"])
df_ideal.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>item</th>
      <th>action</th>
      <th>relevance</th>
      <th>discount_factor</th>
      <th>factor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>50</th>
      <td>9</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.253085</td>
      <td>1.442695</td>
    </tr>
    <tr>
      <th>32</th>
      <td>5</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.283578</td>
      <td>0.910239</td>
    </tr>
    <tr>
      <th>22</th>
      <td>5</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.314658</td>
      <td>0.721348</td>
    </tr>
    <tr>
      <th>23</th>
      <td>1</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.310667</td>
      <td>0.621335</td>
    </tr>
    <tr>
      <th>85</th>
      <td>8</td>
      <td>Ordered</td>
      <td>4</td>
      <td>0.223919</td>
      <td>0.558111</td>
    </tr>
  </tbody>
</table>
</div>



# References

[Back to top](#ranking-metrics)

1. <a id="reference_1"></a> [Ranking Evaluation Metrics for Recommender Systems](https://towardsdatascience.com/ranking-evaluation-metrics-for-recommender-systems-263d0a66ef54)
2. <a id="reference_2"></a>[Demystifying NDCG](https://towardsdatascience.com/demystifying-ndcg-bee3be58cfe0)
