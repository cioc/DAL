import config
import json
from cache import Cache

class Wishes:
  def __init__(self):
    self.config = config.config()
    self.bucketname = self.config['wishes']['bucket'] 
    self.cache = Cache()

  def subsets(self):
    l = self.cache.s3listcontents(self.bucketname)
    o = []
    for i in l:
      o.append(i.key)
    return o

  def iter(self, subset):
    h = self.cache.directhandle(self.bucketname, subset)
    for l in iter(h):
      yield json.loads(l)

  def filter(self, subset, f):
    h = self.cache.directhandle(self.bucketname, subset)
    for l in iter(h):
      j = json.loads(l)
      if f(j):
        yield j

  def byid(self, index):
    (subset, i) = index
    h = self.cache.directhandle(self.bucketname, subset)
    c = 0
    for l in iter(h):
      if c == i:
        return json.loads(l)
      else:
        c += 1
    return None 

  def display(self, items):
    for i in items:
      print i
      
