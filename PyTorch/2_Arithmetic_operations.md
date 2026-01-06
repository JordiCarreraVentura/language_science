# 2. Arithmetic operations

## Summary

| No. | Tags | Code |
| --- | --- | --- |
| 1 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (add, addition)), (math, mathematics) | `x + y` |
| 2 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (subtract)), (math, mathematics) | `x - y` |
| 3 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (multiplication, product)), (math, mathematics) | `x * y` |
| 4 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (fraction, division)), (math, mathematics) | `x / y` |
| 5 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (add, addition)), (vs, memory usage), (math, mathematics) | `x.add_(y)` |
| 6 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (subtract)), (vs, memory usage), (math, mathematics) | `x.sub_(y)` |
| 7 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (multiplication, product)), (vs, memory usage), (math, mathematics) | `x.mul_(y)` |
| 8 | Python, PyTorch, (tutorial, how-to), (arithmetic, operations, vector arithmetic, (fraction, division)), (vs, memory usage), (math, mathematics) | `x.div_(y)` |

## Examples

> Element-wise arithmetic operations on tensors are performed as follows.
>
> All of the operations create new tensors.
>
> In-place operations (that modify the original tensor) are performed using the following methods with the _ suffix, as shown below.


```python
import torch
```


```python
x = torch.tensor([3, 2, 1])
y = torch.tensor([1, 2, 3])
```

### Operations


```python
x + y         # Addition
```




    tensor([4, 4, 4])




```python
x - y    # Subtraction
```




    tensor([ 2,  0, -2])




```python
x * y    # Multiplication
```




    tensor([3, 4, 3])




```python
x / y      # Division
```




    tensor([3.0000, 1.0000, 0.3333])



#### In-place operations


```python
x
```




    tensor([3, 2, 1])




```python
# In-place operations (modifies x)
x.sub_(3)
```




    tensor([ 0, -1, -2])




```python
x
```




    tensor([ 0, -1, -2])


