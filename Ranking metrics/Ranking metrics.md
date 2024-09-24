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

# Examples

[Back to top](#ranking-metrics)


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

    [8, 0, 5, 7, 4, 9, 1, 2, 3, 6]
    [8, 0, 5, 7, 4, 9, 1, 2, 3, 6]
    {8: 1, 0: 1, 5: 1, 7: 1, 4: 1, 9: 0, 1: 0, 2: 0, 3: 0, 6: 0}
    
    [5, 3, 0, 6, 9, 2, 4, 7, 8, 1]
    [5, 3, 0, 6, 9, 2, 4, 7, 8, 1]
    {5: 1, 3: 1, 0: 1, 6: 1, 9: 1, 2: 0, 4: 0, 7: 0, 8: 0, 1: 0}
    
    [9, 0, 3, 1, 4, 8, 7, 2, 6, 5]
    [9, 0, 3, 1, 4, 8, 7, 2, 6, 5]
    {9: 1, 0: 1, 3: 1, 1: 1, 4: 1, 8: 0, 7: 0, 2: 0, 6: 0, 5: 0}
    
    [1, 0, 9, 5, 8, 6, 2, 7, 3, 4]
    [1, 0, 9, 5, 8, 6, 2, 7, 3, 4]
    {1: 1, 0: 1, 9: 1, 5: 1, 8: 1, 6: 0, 2: 0, 7: 0, 3: 0, 4: 0}
    
    [0, 7, 9, 4, 3, 1, 6, 2, 8, 5]
    [0, 7, 9, 4, 3, 1, 6, 2, 8, 5]
    {0: 1, 7: 1, 9: 1, 4: 1, 3: 1, 1: 0, 6: 0, 2: 0, 8: 0, 5: 0}
    
    [9, 6, 7, 0, 1, 8, 2, 5, 3, 4]
    [9, 6, 7, 0, 1, 8, 2, 5, 3, 4]
    {9: 1, 6: 1, 7: 1, 0: 1, 1: 1, 8: 0, 2: 0, 5: 0, 3: 0, 4: 0}
    
    [0, 8, 2, 6, 1, 5, 4, 3, 9, 7]
    [0, 8, 2, 6, 1, 5, 4, 3, 9, 7]
    {0: 1, 8: 1, 2: 1, 6: 1, 1: 1, 5: 0, 4: 0, 3: 0, 9: 0, 7: 0}
    
    [8, 9, 0, 7, 3, 1, 2, 6, 5, 4]
    [8, 9, 0, 7, 3, 1, 2, 6, 5, 4]
    {8: 1, 9: 1, 0: 1, 7: 1, 3: 1, 1: 0, 2: 0, 6: 0, 5: 0, 4: 0}
    
    [1, 3, 8, 4, 5, 6, 9, 7, 2, 0]
    [1, 3, 8, 4, 5, 6, 9, 7, 2, 0]
    {1: 1, 3: 1, 8: 1, 4: 1, 5: 1, 6: 0, 9: 0, 7: 0, 2: 0, 0: 0}
    
    [2, 6, 0, 5, 1, 7, 4, 9, 3, 8]
    [2, 6, 0, 5, 1, 7, 4, 9, 3, 8]
    {2: 1, 6: 1, 0: 1, 5: 1, 1: 1, 7: 0, 4: 0, 9: 0, 3: 0, 8: 0}
    



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

    1.0
    1.0
    0.8


# References

[Back to top](#ranking-metrics)

1. <a id="reference_1"></a> [Ranking Evaluation Metrics for Recommender Systems](https://towardsdatascience.com/ranking-evaluation-metrics-for-recommender-systems-263d0a66ef54)
2. <a id="reference_2"></a>[Demystifying NDCG](https://towardsdatascience.com/demystifying-ndcg-bee3be58cfe0)
