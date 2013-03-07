import config
from cache import Cache
from s3iterable import S3Iterable

class Sou(S3Iterable):
  def __init__(self):
    super(Sou, self).__init__() 
    self.config = config.config()
    self.bucketname = self.config['sou']['bucket'] 
