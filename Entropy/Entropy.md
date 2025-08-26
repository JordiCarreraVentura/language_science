```python
%load_ext autoreload
%autoreload
    
from math import log
from typing import *

import pandas as pd
from IPython.display import display, Markdown
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
def entropy(ratios: List[float]) -> float:
    information = [
        round(log(ratio), 2)
        for ratio in ratios
    ]
    information_times_ratio = [
        round(ratio * log(ratio), 2)
        for ratio in ratios
    ]
    return information, information_times_ratio, round(-sum([
        round(ratio * log(ratio), 2)
        for ratio in ratios
    ]), 2)
```

# Entropy

The formula of entropy is given below:

$$Entropy(S) = - \sum_{i=1}^{c}{p_i log_2(p_i)}$$

## Discussion

1. _Is $p_i$ a probability?_

   No, it is not. While it is expressed as a polarity, it is actually just a ratio and it corresponds to $$n_c / |N| = n_c / |\forall_{c' \in C}^{C}\ n_{c'}|,$$ or the number of elements in each class $c$ divided over the total number of elements (for any class). Essentially, it tells us which fraction of a dataset (or subset thereof) belongs to each class.
2. _Why do we use the **unary negation** to reverse the polarity?_

   Because the logarithm inside the summation yields negative numbers, yet the entropy is defined as a positive magnitude (a concave function that we intend to maximize, insofar as we are measuring the presence of something). To get a positive measurament (corresponding to the presence of something) on the basis of negative values (typically associated with the absence of something), we need to reverse their polarity. And we cannot just add some other value to it because that would effectively cancel them out.
4. _Why do we use the logarithm?_

   It provides re-scaling of a fraction that is beyond normalization and, in that way, reinstates a sense of an absolute value. Fractions are relative and will always add up to $1.0$, which would be ambiguous between all possible distributions of the classes (all combinations of fractional numbers add up to $1.0$ when expressing probabilities or ratios).

   In contrast, $log(1/2) \approx -0.3$ and $log(1/4) \approx -0.6$. Hence, assuming $n = |2|$ and $n = |4|$, respectively (under the uniformity assumption), the sum of their entropies is $-0.6$ and $-2.4$, despite the fact that the sum of the ratios themselves would still be $1.0$ and $1.0$, and non-differentiable. **The logarithm makes these ratios differentiable**, still as a function of their **original proportion** as ratios, while also magnifying the result for smaller ratios because, by the definition of entropy, **lower ratios represent a lower expectation** and must therefore be assigned a higher entropy. The (negative) logarithm over-represents smaller values because, for a small ratio, it is orders of magnitude greater than the ratio itself, e.g.


```python
for val in [0.9, 0.1, 0.01, 0.001]:
    print('{:<7.3f}{:<7.2f}{:>10.2f}'.format(val, log(val), log(val) / val))
```

    0.900  -0.11       -0.12
    0.100  -2.30      -23.03
    0.010  -4.61     -460.52
    0.001  -6.91    -6907.76


<p style="margin-left: 30px;">In this respect, the logarithm provides a straightforward interpretation in terms of information theory. Refer to appendix <i>Information-theoretical Interpretation of the Logarithm</i> for an explanation.</p>

5. _Why do we multiply the logarithm of $p_i$ times $p_i$ again?_

   Because its innermost usage will have transformed the ratio into a measure of information which _is based_ on the original ratio (actually, information $I$ is defined precisely as $-log(p_i)$) but is **no longer reflective of its overall weight** on the original dataset. Hence, we can have classes with a very low ratio and, as a result, extremely high information, yet they are so rare that their total contribution to the entropy could still be low. The highest entropies will normally be measured over ratios that are low yet still significant (closer to the random baseline, or $1 / |C|$).
    For example, 


```python
ratio_sets = [
    ([round(1/3, 2) for _ in range(3)], 'Maximum entropy distribution following a uniform assumption.'),
    ([0.3, 0.3, 0.4], 'Multiple ratios close to each other: we expect very high entropy in this case.'),
    ([0.7, 0.25, 0.05], 'Skewed distribution with two clear most and least frequent classes. We expect a lower entropy here.'),
    ([0.9, 0.09, 0.01], 'An even more skewed distribution, which we expect to have the lowest entropy of all three.')
]

for ratios, explanation in ratio_sets:
    information, information_times_ratio, total_entropy = entropy(ratios)

    schema = ['Class ratios: '] + ratios
    row0 = ['information='] + information
    row1 = ['information times ratio='] + information_times_ratio
    row2 = ['entropy='] + [total_entropy] + ['' for _ in range(len(information) - 2)] + [f'-----> {explanation}']
    
    df = pd.DataFrame([row0, row1, row2], columns=schema)

    display(Markdown(df.to_markdown(index=False)))
```


| Class ratios:            |   0.33 | 0.33   | 0.33                                                                |
|:-------------------------|-------:|:-------|:--------------------------------------------------------------------|
| information=             |  -1.11 | -1.11  | -1.11                                                               |
| information times ratio= |  -0.37 | -0.37  | -0.37                                                               |
| entropy=                 |   1.11 |        | -----> Maximum entropy distribution following a uniform assumption. |



| Class ratios:            |   0.3 | 0.3   | 0.4                                                                                   |
|:-------------------------|------:|:------|:--------------------------------------------------------------------------------------|
| information=             | -1.2  | -1.2  | -0.92                                                                                 |
| information times ratio= | -0.36 | -0.36 | -0.37                                                                                 |
| entropy=                 |  1.09 |       | -----> Multiple ratios close to each other: we expect very high entropy in this case. |



| Class ratios:            |   0.7 | 0.25   | 0.05                                                                                                       |
|:-------------------------|------:|:-------|:-----------------------------------------------------------------------------------------------------------|
| information=             | -0.36 | -1.39  | -3.0                                                                                                       |
| information times ratio= | -0.25 | -0.35  | -0.15                                                                                                      |
| entropy=                 |  0.75 |        | -----> Skewed distribution with two clear most and least frequent classes. We expect a lower entropy here. |



| Class ratios:            |   0.9 | 0.09   | 0.01                                                                                              |
|:-------------------------|------:|:-------|:--------------------------------------------------------------------------------------------------|
| information=             | -0.11 | -2.41  | -4.61                                                                                             |
| information times ratio= | -0.09 | -0.22  | -0.05                                                                                             |
| entropy=                 |  0.36 |        | -----> An even more skewed distribution, which we expect to have the lowest entropy of all three. |


# Appendix

## Information-theoretical Interpretation of the Logarithm

<a id="information_theoretical_interpretation"></a>

> When working with fractions (probabilities), we want to quantify how surprising or uncertain something is.
> The log does this because it grows slowly and fits the idea of measuring "information in bits":
> 
> $$I(p)=−log_2(p)$$
> 
> - If $p=1$ (certain), then I=0 bits (no surprise).
> - If $p=\frac{1}{2}$, then I=1 bit (like flipping a fair coin).
> - If $p=\frac{1}{4}$, then I=2 bits.
> 
> So the log maps fractions between 0 and 1 to meaningful, additive "information quantities."
