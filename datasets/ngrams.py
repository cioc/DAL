import config
import json
from cache import Cache
from s3iterable import S3Iterable

def parsegram(l):
  pieces = l.split('\t')
  pieces[1] = int(pieces[1])
  pieces[2] = int(pieces[2])
  pieces[3] = int(pieces[3])
  pieces[4] = int(pieces[4].strip())
  return pieces

class Ngrams(S3Iterable):
  def __init__(self):
    super(Ngrams, self).__init__() 
    self.config = config.config()
    self.bucketname = self.config['ngrams']['bucket']
    self.parser = parsegram
    self.decompress = "unzip" 
