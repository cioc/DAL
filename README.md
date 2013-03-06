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
* Wishes ('wishes')
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

Tiny images features a search command that takes in a keyword and limit and will return up to limit image indices associated with the keyword.

```python
def search(keyword, limit)
```

Wishes - DSA
============

Returns a listing of the subsets of wishes.  Each represents a day's or a subset of a day's wishes.

```python
def subsets(self)
```

Using the identifiers from a call to subsets, you can call iter on a subset of the wishes.  Iter returns an iterator that allows you to iterate over the entire subset.

```python
def iter(self, subset)
```

Filter is just like iter except it also takes in a function, f, that used to filter the items returned by the iterator.  Only items that return true when passed into f will be returned.

```python
def filter(self, subset, f)
```


