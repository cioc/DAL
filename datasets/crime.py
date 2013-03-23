import config
import json
from cache import Cache
from s3iterable import S3Iterable

class Crime(S3Iterable):
  def __init__(self):
    super(Crime, self).__init__() 
    self.config = config.config()
    self.bucketname = self.config['crime']['bucket']
    self.decompress = "unzip"
  
  def metadata(self, subset):
    dh = self.cache.directhandle(self.bucketname, subset)
    return json.loads(dh.read()) 
