import numpy
import scipy
import Image

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
    self.meta = open(self.config['tinyimages']['metapath'], 'rb')
    self.data = open(self.config['tinyimages']['datapath'], 'rb')
    self.img_count = 79302017
 
  #public functions
  def byid(self, ids):
    if isinstance(ids, int):
      offset = ids * 3072
      self.data.seek(offset)
      data = self.data.read(3072)
      return numpy.fromstring(data, dtype='uint8')    
    elif isinstance(ids, tuple):
      (start, end) = ids
      offset = start * 3072
      self.data.seek(offset)
      data = self.data.read((end - start) * 3072)
      pos = 0
      dlen = len(data)
      o = []
      while pos < dlen:
        stop = pos + 3072
        o.append(numpy.fromstring(data[pos:3072], dtype='uint8'))
        pos += 3072
      return o
    else:
      o = []
      for i in ids:
        offset = i * 3072
        self.data.seek(offset)
        data = self.data.read(3072)
        o.append(numpy.fromstring(data, dtype='uint8'))  
      return o

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
    offset = index * 768
    self.meta.seek(offset)
    data = self.meta.read(768)
    return data[0:80].strip()

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
