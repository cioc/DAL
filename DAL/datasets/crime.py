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
    df = self.cache.directhandle(self.bucketname, 'dfnk-7re6.json.meta.json', decompress=None)
    ij = self.cache.directhandle(self.bucketname, 'ij.source.meta.meta.json', decompress=None)
    o = {}
    o['dfnk-7re6.json.meta.json'] = json.loads(df.read())
    o['ij.source.meta.meta.json'] = json.loads(ij.read())
    return o
