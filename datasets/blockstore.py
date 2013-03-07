class BlockStore(object):
  def __init__(self, filename, blocksize):
    self.path = filename
    self.blocksize = blocksize
  
  def slice(self, start, end):
    f = open(self.path, 'rb')
    curr = start
    f.seek(start * self.blocksize)
    while curr <= end:
      yield f.read(self.blocksize) 
      curr += 1 
    f.close()
  def byid(self, id):
    f = open(self.path, 'rb')
    f.seek(id *self.blocksize)
    o = f.read(self.blocksize)
    f.close()
    return o
