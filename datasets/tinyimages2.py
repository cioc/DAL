import config
import json
import math
import numpy
from cache import Cache
from s3iterable import S3Iterable

class TinyImages2(S3Iterable):
  def __init__(self):
    super(TinyImages2, self).__init__() 
    self.config = config.config()
    self.bucketname = self.config['tinyimages2']['bucket'] 
    self.parser = json.loads

  def byid(self, index):
    block = int(math.floor(index / 3400))
    print str(block)+'.part'
    h = self.cache.directhandle(self.bucketname, str(block)+'.part',binary=True)
    offset = (index % 3400) * 3072
    h.seek(offset)
    o = h.read(3072) 
    h.close()
    return numpy.fromstring(o, dtype='uint8')
