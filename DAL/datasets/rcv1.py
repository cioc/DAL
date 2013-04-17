import config
import json
from cache import Cache
from s3iterable import S3Iterable

class rcv1(S3Iterable):
  def __init__(self):
    super(rcv1, self).__init__() 
    self.config = config.config()
    if config.local():
      self.bucketname = self.config['rcv1']['bucket']+'-local'
    else:
      self.bucketname = self.config['rcv1']['bucket']
    self.parser = json.loads
    self.decompress = "unzip" 
