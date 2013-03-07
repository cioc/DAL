import numpy
import scipy
import Image
from blockstore import BlockStore
import config

#TODO - try to remove
def _strcmp(str1, str2):
  l = min(len(str1), len(str2)) 
  for i in range(0, l):
    if (ord(str1[i]) > ord(str2[i])):
      return 1
    if (ord(str1[i]) < ord(str2[i])):
      return -1
  if (len(str1) > len(str2)):
    return 1
  if (len(str1) < len(str2)):
    return -1
  return 0   

class TinyImage:
  def __init__(self):
    self.config = config.config()  
    self.meta = BlockStore(self.config['tinyimages']['metapath'], 768)
    self.data = BlockStore(self.config['tinyimages']['datapath'], 3072) 
    self.img_count = 79302017
 
  #public functions
  def byid(self, ids):
    if isinstance(ids, int):
      for s in self.data.slice(ids, ids): 
        return numpy.fromstring(s, dtype='uint8')    
    elif isinstance(ids, tuple):
      o = []
      for s in self.data.slice(ids[0], ids[1]):
        o.append(numpy.fromstring(s, dtype='uint8'))
      return o 
    else:
      o = []
      for i in ids:
        o.append(numpy.fromstring(self.data.slice(i, i), dtype='uint8'))  
      return o

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
    
  def search(self, keyword, limit):
    (l, h) = self._logSearch(keyword)
    found = False
    found_count = 0
    o = []
    for i in range(l, h):
      curr_word = self._keywordFromMeta(i)
      if curr_word.lower() == keyword.lower():
        found = True
        o.append(i)
        found_count += 1
        if (found_count == limit):
          break
      else:
        if (found):
          break  
    return o

  def _keywordFromMeta(self, index):
    for s in self.meta.slice(index, index):
      return s[0:80].strip()

  def _logSearch(self, term):
    low = 0
    high = self.img_count
    for i in range(0, 9):
      curr_word = self._keywordFromMeta(int((low + high) / 2))
      cmp = _strcmp(curr_word.lower(), term.lower())
      if (cmp == 0):
        return (low, high)
      if (cmp == 1):
        high = ((low + high) / 2)
      if (cmp == -1):
        low = ((low + high) / 2)
    return (low, high)

  def subsets(self):
    return None
