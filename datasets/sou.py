import config
from cache import Cache
from s3iterable import S3Iterable

class Sou(S3Iterable):
  def __init__(self):
    super(Sou, self).__init__() 
    self.config = config.config()
    if config.local():
      self.bucketname = self.config['sou']['bucket']+'-local'
    else:
      self.bucketname = self.config['sou']['bucket']
  def metadata(self):
    dh = self.cache.directhandle(self.bucketname, 'soumeta.txt')
    o = []
    for l in dh:
      p = l.split('|')
      o.append((p[0],p[1],int(p[2])))
    return o
