import config
import pickle 
import os.path
from boto.s3.connection import S3Connection
from boto.s3.key import Key

#TODO - size handling
def parseSize(s):
  pass

class Cache:
  def __init__(self):
    self.config = config.config()
    self.path = self.config['cache']['path']
    self.aws_access_key = self.config['cache']['AWS_ACCESS_KEY']
    self.aws_secret_key = self.config['cache']['AWS_SECRET_KEY']
    self.size = parseSize(self.config['cache']['size'])
    self.entries = {}
    self.entrylog = open(self.path+'/cache.log', "a") 
    self._loadlog()

  def s3listcontents(self, bucketname):
    conn = S3Connection(self.aws_access_key, self.aws_secret_key)
    b = conn.get_bucket(bucketname)
    o = b.list()
    conn.close()
    return o
  
  def s3tocache(self, bucketname, objname):
    conn = S3Connection(self.aws_access_key, self.aws_secret_key)
    b = conn.get_bucket(bucketname)
    k = Key(b)
    k.key = objname
    k.get_contents_to_filename(self.path+'/'+objname) 
  
  def incache(self, objname):
    return os.path.isfile(self.path+'/'+objname) 
    
  def directhandle(self, bucketname, objname):
    if self.incache(objname):
      return open(self.path+'/'+objname)
    else:
      self.s3tocache(bucketname, objname)
      return open(self.path+'/'+objname) 

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
