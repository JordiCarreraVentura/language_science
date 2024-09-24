# Ranking metrics

1. [Online metrics](#online-metrics)
   1. [Hit ratio](#hit-ratio)
2. [Offline metrics](#offline-metrics)
   1. [Reciprocal rank and Mean reciprocal rank](#reciprocal-rank)

## Online metrics

### Hit ratio

[Source](#reference_1)

> the fraction of users for which the correct answer is included in the recommendation list of length $L$.

$D = \text{every set of recommendations }d\text{ served ot a user, such that }|d| = L$

$y = \text{the correct answer}$

$$HR_L = \frac{|d: d \in D \land y \in d|}{|D|}$$

**NOTE**: $L$ is a parameter.

## Offline metrics

### Reciprocal rank and Mean reciprocal rank

[Source](#reference_1)

$D = \text{every set of recommendations }d\text{ served ot a user, such that }|d| = L$

$$RR(d) = \sum\limits_{i: 1 ≤ i ≤ L} \frac{relevance_i}{rank_i}$$

$$MRR(D) = \frac{ \sum\limits_{i = 1}^{|D|} RR(D_i) }{|D|} $$

**NOTE**: _one could argue that hit ratio is actually a special case of MRR in which RR(d) is binary, as it becomes 1 if there is a relevant item in the list, 0 otherwise._


```python

```

# References

1. <a id="reference_1"></a> [Ranking Evaluation Metrics for Recommender Systems](https://towardsdatascience.com/ranking-evaluation-metrics-for-recommender-systems-263d0a66ef54)
2. <a id="reference_2"></a>[Demystifying NDCG](https://towardsdatascience.com/demystifying-ndcg-bee3be58cfe0)
