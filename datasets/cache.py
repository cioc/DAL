import config
import pickle 

#TODO - size handling
def parseSize(s):
  pass

class Cache:
  def __init__(self):
    self.config = config.config()
    self.path = self.config['cache']['path']
    self.size = parseSize(self.config['cache']['size'])
    self.entries = {}
    self.entrylog = open(self.path+'/cache.log', "a") 
    self._loadlog()
     
  def store(self, groupname, id, obj):
    if isinstance(id, int):
      path = '%s/%s-%d.obj' % (self.path, groupname, id)
    elif isinstance(id, tuple):
      (start, end) = id
      path = '%s/%s-(%d,%d)' % (self.path, groupname, start, end)
    else:
      raise Exception("cache only stores individual objs and intervals")    
    if groupname not in self.entries:
      self.entries[groupname] = [id]
    else:
      self.entries[groupname].append(id) 
    f = open(path, "w")
    f.write(pickle.dumps(obj))
    f.close() 
    self._log(groupname, id)

  def _loadlog(self):
    f = open(self.path+'/cache.log', 'r')
    for l in f.readlines():
      pieces = l.split(' ')
      if len(pieces) == 2:
        if pieces[0] not in self.entries:
          self.entries[pieces[0]] = []
        self.entries[pieces[0]].append(int(pieces[1]))
      elif len(pieces) == 3:
        if pieces[0] not in self.entries:
          self.entries[pieces[0]] = []
        self.entries[pieces[0]].append((int(pieces[1]), int(pieces[2]))) 
      else:
        raise Exception('Invalid cache.log')
    f.close()

  def _log(self, groupname, identifier):
    if isinstance(identifier, int):
      entry = '%s %d\n' % (groupname, identifier)
    elif isinstance(identifier, tuple):
      (start, end) = identifier
      entry = '%s %d %d\n' % (groupname, start, end)
    else:
      raise Exception("Not proper log entry") 
    self.entrylog.write(entry)
  
  def load(self, groupname, id):
    if groupname not in self.entries:
      return None
    if isinstance(id, int): 
      for i in self.entries[groupname]:
        if isinstance(i, tuple):
          (start, end) = i
          if id >= start and id <= end:
            path = '%s/%s-(%d,%d)' % (self.path, groupname, start, end)   
            f = open(path, "r")
            d = pickle.loads(f.read())
            f.close()
            return d[id - start] 
        else:
          if id == i: 
            path = '%s/%s-%d.obj' % (self.path, groupname, id)
            f = open(path, "r")
            d = pickle.loads(f.read())
            f.close()
            return d
    elif isinstance(id, tuple):
      for i in self.entries[groupname]:
        if isinstance(i, tuple):
          (start, end) = i
          (tstart, tend) = id
          if tstart >= start and tend <= end:
            path = '%s/%s-(%d,%d)' % (self.path, groupname, start, end)   
            f = open(path, "r")
            d = pickle.loads(f.read())
            f.close()
            return d[tstart:(tend + 1)] 
    else:
      return None
    
c = Cache()
#x = [1,2,3,4,5,6,7]
#z = [11,12,13,14,15]
#c.store('testgroup', (0, 6), x)
#c.store('othergroup', 0, z)
#y = c.load('othergroup', 0)
#print y
 
