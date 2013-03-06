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
    if self.cache.incache(subset):
      h = self.cache.directhandle(subset)
    else:
      self.cache.s3tocache(self.bucketname, subset)
      h = self.cache.directhandle(subset)
    for l in iter(h):
      yield json.loads(l)

  def filter(self, subset, f):
    if self.cache.incache(subset):
      h = self.cache.directhandle(subset)
    else:
      self.cache.s3tocache(self.bucketname, subset)
      h = self.cache.directhandle(subset)
    for l in iter(h):
      j = json.loads(l)
      if f(j):
        yield j


  def byid(self):
    pass

  def display(self):
    pass
