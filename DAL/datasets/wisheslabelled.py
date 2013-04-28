import config
import json
from cache import Cache
from s3iterable import S3Iterable

class WishesLabelled(S3Iterable):
  def __init__(self):
    super(WishesLabelled, self).__init__() 
    self.config = config.config()
    if config.local():
      self.bucketname = self.config['wishes-labelled']['bucket']+'-local' 
    else:
      self.bucketname = self.config['wishes-labelled']['bucket']
    self.parser = json.loads
