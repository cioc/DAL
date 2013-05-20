import config
import json
import pickle
from cache import Cache
from s3iterable import S3Iterable

class LightCurves(S3Iterable):
  def __init__(self,original=None):
    super(LightCurves, self).__init__() 
    self.config = config.config()
    if config.local():
      self.bucketname = self.config['lightcurves']['bucket']+'-local'
    else:
      self.bucketname = self.config['lightcurves']['bucket']
    if original is not None:
      self.bucketname = 'ml-lightcurves-q14' 
    self.decompress = "unzip"
    self.parser = None

  def iter(self, subset):
    accum = ""
    for i in super(LightCurves, self).iter(subset):
      v = i.strip()
      if v == '<I1N2D3I4C5A6T7O8R9>':
        if accum.strip() != "":
          yield json.loads(accum)
        accum = ""  
      else:
        accum += i
    if accum != '':
      yield json.loads(accum)
      accum = ""
  
  def filter(self, subset, f):
    for i in self.iter(subset):
      if f(i):
        yield i
