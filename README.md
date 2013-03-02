Data Access Layer (DAL) for lsdacluster
=======================================

The data access layer (DAl) makes working with lsdacluster's large datasets much easier.  It does this by transparently exposing the datasets with a relatively uniform API.

Example usage
=============

```python
from DAL import create
#create a handle to the tinyimages dataset
tinyimages = create('tinyimages')

#load in tinyimages 0 through 99
x = tinyimages.byid((0, 100))

#display those images
tinyimages.display(x)
```

Data set handles
================

A handle to a dataset is returned by called the create method with the name of the dataset as the parameter.

```python
def create(name)
```

Currently supported datasets:

* Tiny Images ('tinyimages')
* Cache (to be determined)

Uniform Api
===========

Each dataset must have two methods: byid and display.

```python
def byid (index OR (start, end) OR [indices])

def display(array)
```

byid takes in an index (integer) a (start, end) pair or an array of indices and returns the associated data items.

display takes in an array of dataitems and displays them in an ipython notebook.

Tiny Images - Dataset Specific API (DSA)
========================================

```python
def search(keyword, limit)
```

Tiny images features a search command that takes in a keyword and limit and will return up to limit image indices associated with the keyword.



