import config
from cache import Cache

class S3Iterable(object):
  def __init__(self):
    '''
    Subclasses must handle setting up config including:
    * bucketname
    * parser
    '''
    self.bucketname = None
    self.parser = None
    self.cache = Cache()
    self.iterator = iter
    self.decompress = None

  def subsets(self):
    l = self.cache.s3listcontents(self.bucketname)
    o = []
    for i in l:
      o.append(i.key)
    return o

  def iter(self, subset):
    if self.decompress is not None:
      h = self.cache.directhandle(self.bucketname, subset, decompress=self.decompress)
    else:
      h = self.cache.directhandle(self.bucketname, subset)
    for l in self.iterator(h):
      if self.parser is None:
        yield l
      else:
        yield self.parser(l)

  def filter(self, subset, f):
    h = self.cache.directhandle(self.bucketname, subset)
    for l in self.iterator(h):
      if self.parser is None:
        j = l
      else:
        j = self.parser(l)
      if f(j):
        yield j

  def byid(self, index):
    (subset, i) = index
    h = self.cache.directhandle(self.bucketname, subset)
    c = 0
    for l in self.iterator(h):
      if c == i:
        if self.parser is None:
          return l
        else:
          return self.parser(l)
      else:
        c += 1
    return None 

  def display(self, items):
    for i in items:
      print i
 
