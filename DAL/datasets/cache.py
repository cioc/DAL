import config
import pickle 
import os
import os.path
import subprocess
import fcntl
import time
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import czipfile as zipfile
from collections import defaultdict

#TODO - size handling
def parseSize(s):
  pass

def decompress_name(name):
  pieces = name.split('.')
  return '.'.join(pieces[:(len(pieces) - 1)])

def storage_name(path, name, bucketname):
  return path+'/' + bucketname+'-'.join(name.split('/'))
 
class Cache:
  def __init__(self):
    self.config = config.config()
    self.path = self.config['cache']['path']
    self.aws_access_key = self.config['cache']['AWS_ACCESS_KEY']
    self.aws_secret_key = self.config['cache']['AWS_SECRET_KEY']
    self.size = parseSize(self.config['cache']['size'])

  def s3listcontents(self, bucketname):
    conn = S3Connection(self.aws_access_key, self.aws_secret_key)
    b = conn.get_bucket(bucketname)
    o = b.list()
    conn.close()
    return o
  
  def s3tocache(self, bucketname, objname, decompress=None):
    r = self.__lockOrNone(bucketname, objname)
    if r is None:
      while (self.__getStateFromLog(bucketname, objname) == "downloading..."):
        time.sleep(1)
    else:
      conn = S3Connection(self.aws_access_key, self.aws_secret_key)
      b = conn.get_bucket(bucketname)
      k = Key(b)
      k.key = objname
      path = storage_name(self.path, objname, bucketname)
      k.get_contents_to_filename(path)
      if decompress is not None:
        self.decompress(decompress, path) 
      self.__logWithLock(bucketname, objname, "COMPLETE")
       
  def decompress(self, cmd, path):
    decompath = decompress_name(path)
    if (os.path.isfile(decompath)):
      return decompath
    if cmd == 'unzip':
      z = zipfile.ZipFile(path)
      p = decompath.split('/')
      z.extractall(path=self.path)
      n = z.namelist()[0]
      os.rename('/mnt/'+n, decompath)
    else:
      raise Exception("No Such Decompressor")
    return decompath
  
  def cleancache(self):
    if os.path.exists(self.path+'/cache.log'): 
      state = defaultdict(lambda: [])
      with open(self.path+'/cache.log', 'r') as f:
        for l in f:
          pieces = l.split()
          if len(l) > 0 and len(pieces) == 3:
            pieces = l.split()
            k = pieces[0] + '|' +pieces[1]
            state[k].append(pieces[2])
      with open(self.path+'/cache.log', 'w') as f:
        for k, v in state.iteritems():
          if 'downloading...' in v and 'COMPLETE' in v:
            pieces = k.split('|')
            f.write(pieces[0] + ' ' + pieces[1] + ' ' + 'downloading...\n')
            f.write(pieces[0] + ' ' + pieces[1] + ' ' + 'COMPLETE\n')
  
  def directhandle(self, bucketname, objname, decompress=None, binary=None):
    if decompress is None:
      path = storage_name(self.path, objname, bucketname)
    else:
      path = decompress_name(storage_name(self.path, objname, bucketname))
    if os.path.isfile(path) and self.__getStateFromLog(bucketname, objname) == "COMPLETE":
      if binary is not None:
        return open(path, 'rb')
      else:
        return open(path)
    else:
      self.s3tocache(bucketname, objname, decompress=decompress)
      if binary is not None:
        return open(path, 'rb')
      else:
        return open(path)
  
  def __getStateFromLog(self, bucketname, objname):
    foundDownload = False
    entrylog = open(self.path+'/cache.log', "a+") 
    for l in entrylog:
      pieces = l.split(" ")
      if pieces[0] == bucketname and pieces[1] == objname:
        if pieces[2].strip() == "COMPLETE":
          return "COMPLETE"
        else:
          foundDownload = True
    if foundDownload:
      return "downloading..."
    return None 
   
  def __lockOrNone(self, bucketname, obj):
    entrylog = open(self.path+'/cache.log', "a+") 
    fcntl.flock(entrylog.fileno(), fcntl.LOCK_EX)
    state = self.__getStateFromLog(bucketname, obj)
    if state is None:
      self.__log(bucketname, obj, "downloading...")
      fcntl.flock(entrylog.fileno(), fcntl.LOCK_UN)
      return "downloading..."
    fcntl.flock(entrylog.fileno(), fcntl.LOCK_UN)
    entrylog.close()
    return None 

  def __logWithLock(self, bucketname, objname, state):
    entrylog = open(self.path+'/cache.log', "a+") 
    fcntl.flock(entrylog.fileno(), fcntl.LOCK_EX)
    entry = "%s %s %s" % (bucketname, objname, state)
    entrylog.write(entry+'\n')    
    fcntl.flock(entrylog.fileno(), fcntl.LOCK_UN)
    entrylog.close()

  def __log(self, bucketname, objname, state):
    entrylog = open(self.path+'/cache.log', "a+") 
    entry = "%s %s %s" % (bucketname, objname, state)
    entrylog.write(entry+'\n')   
    entrylog.close() 
