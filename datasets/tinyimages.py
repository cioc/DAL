import config
import json
import math
import numpy
from cache import Cache
from s3iterable import S3Iterable

# "meta-bucket": "ml-tinyimages-metadata"
class TinyMetaData(S3Iterable):
  def __init__(self):
    super(TinyMetaData, self).__init__() 
    self.config = config.config()
    self.bucketname = self.config['tinyimages']['meta-bucket'] 
    self.parser = json.loads
    self.img_count = 79302017
        
  def byid(self, index):
    if index < 0 or index > self.img_count:
      raise IndexError("Index must be between 0 and %d" % (self.img_count))
    block = int(math.floor(index / 3400))
    h = self.cache.directhandle(self.bucketname, str(block)+'.part',binary=True)
    offset = (index % 3400) * 768
    h.seek(offset)
    o = h.read(768) 
    h.close()
    return numpy.fromstring(o, dtype='uint8')

  def keyword(self, index):
    d = self.byid(index)
    return d[:80].tostring().strip()

class TinyImages(S3Iterable):
  def __init__(self):
    super(TinyImages, self).__init__() 
    self.config = config.config()
    self.bucketname = self.config['tinyimages']['bucket'] 
    self.parser = json.loads
    self.img_count = 79302017    
    self.metadata = TinyMetaData()
  
  def search(self, keyword, limit):
    h = self.img_count
    l = 0
    while (h > l):
      m = (h + l) / 2
      k = self.metadata.keyword(m)
      if keyword.lower() == k.lower():
        o = []
        c = 0
        s = m
        while self.metadata.keyword(s) == keyword:
          s -= 1
        s += 1 
        while (self.metadata.keyword(s) == keyword) and (c < limit):
          o.append(s)
          c += 1
          s += 1
        return o 
      elif keyword.lower() < k.lower():
        h = m
      else:
        l = m
    return [-1] 
        
  def display(self, items):
    import cStringIO as StringIO
    import base64
    from IPython.core.display import HTML
    output_html = ""
    for i in items:
      t = i.reshape(32,32,3, order="F").copy()
      img = scipy.misc.toimage(t) 
      output = StringIO.StringIO()
      img.save(output, format="PNG")
      output_html += '<img src="data:image/png;base64,%s"/>' % base64.b64encode(output.getvalue())
    return HTML(output_html) 

  def byid(self, indexes):
    if isinstance(indexes, int):
      return self.__byid(indexes) 
    elif isinstance(indexes, tuple):
      o = []
      for i in xrange(indexes[0], indexes[1]):
        o.append(self.__byid(i))
      return o
    else:
      o = []
      for i in indexes:
        o.append(self.__byid(i))
      return o

  def __byid(self, index):
    if index < 0 or index > self.img_count:
      raise IndexError("Index must be between 0 and %d" % (self.img_count))
    block = int(math.floor(index / 3400))
    h = self.cache.directhandle(self.bucketname, str(block)+'.part',binary=True)
    offset = (index % 3400) * 3072
    h.seek(offset)
    o = h.read(3072) 
    h.close()
    return numpy.fromstring(o, dtype='uint8')
