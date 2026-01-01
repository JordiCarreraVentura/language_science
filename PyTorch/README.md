# PyTorch tutorial

## Source

[20 PyTorch Concepts, Explained Simply](https://www.intoai.pub/p/pytorch-essentials)

## Initialization

### 1. Create virtual environment

```
$ make install
```

The command above will also install the dependencies in `requirements.txt` implicitly.

The resulting virtual environment is then expected to be installed as a Jupyter kernel for use on the Jupyter notebooks linked to below (currently, the kernel must be installed manually).

Once the kernel is installed, the command below will launch the server using the Jupyter dependency previously installed as one of the requirements.


### 2. Launch a Jupyter server with the 

```
$ make jupyter
```

## Summaries

### 1. Tensors

- [Jupyter notebook](1_Tensor.ipynb)
- [Section in the original post](https://www.intoai.pub/i/178246834/tensor)

| No. | Code | Tags | Description |
| --- | --- | --- | --- |
| 1 | `torch.tensor(list)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (from, list)) | Initialize a PyTorch tensor from a Python list. |
| 2 | `torch.arange(start: int, end: int, step: int)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (from, range)) | Initialize a PyTorch tensor from a Python range. |
| 3 | `torch.empty(rows: int, columns: int)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (with, null, as, not, values)) | Initialize an empty tensor of the specified shape. |
| 4 | `torch.zeros(rows: int, columns: int)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (with, zeros)) | Like `empty`, but initializing with $0$s instead of null values. |
| 5 | `torch.ones(rows: int, columns: int)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (with, multiple, one)) | Like `empty`, but initializing with $1$s instead. |
| 6 | `torch.rand(rows: int, columns: int)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (with, random, float, numbers, (from, statistics, probability, distribution, uniform, distribution))) | Like `empty`, but initializing with random decimal numbers sampled from a **uniform distribution** instead. |
| 7 | `torch.rand(rows: int, columns: int)` | Python, PyTorch, (tutorial, how-to), (tensor, initialization, (with, random, float, numbers, (from, statistics, probability, distribution, normal distribution))) | Like `empty`, but initializing with random decimal numbers sampled from a **normal distribution** instead. |


