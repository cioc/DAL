import config
import json
from cache import Cache
from s3iterable import S3Iterable

class Crime(S3Iterable):
  def __init__(self):
    super(Crime, self).__init__() 
    self.config = config.config()
    if config.local():
      self.bucketname = self.config['crime']['bucket']+'-local'
    else:
      self.bucketname = self.config['crime']['bucket']
    self.decompress = "unzip"
  
  def metadata(self):
    #dfnk-7re6.json.meta.json => set0
    #ij.source.meta.meta.json => set1
    df = self.cache.directhandle(self.bucketname, 'set0.meta.json', decompress=None)
    ij = self.cache.directhandle(self.bucketname, 'set1.meta.json', decompress=None)
    o = {}
    o['set0.meta.json'] = json.loads(df.read())
    o['set1.meta.json'] = json.loads(ij.read())
    return o
