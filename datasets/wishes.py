import config
import json
from cache import Cache
from s3iterable import S3Iterable

class Wishes(S3Iterable):
  def __init__(self):
    self.config = config.config()
    self.bucketname = self.config['wishes']['bucket'] 
    super(Wishes, self).__init__() 
