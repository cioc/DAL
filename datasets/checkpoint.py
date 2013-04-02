'''
A simple checkpointing system whose store is s3. Built on top of boto.
'''

import os
import boto
from boto.s3.key import Key
import pickle
import config

class Checkpoint:
  def __init__(self):
    self.config = config.config()
    self.bucket = self.config['checkpoint']['bucket']
    self.access_key = self.config['cache']['AWS_ACCESS_KEY']
    self.secret_key = self.config['cache']['AWS_SECRET_KEY']
     
  def store(self, key, obj=None, s=None, fp=None):
    if all([obj is None, s is None, fp is None]):
      raise Exception("o, s, or f must be set")
    conn = boto.connect_s3(self.access_key, self.secret_key)
    bucket = conn.get_bucket(self.bucket)
    k = Key(bucket)
    k.key = key
    if obj is not None:
      k.set_contents_from_string(pickle.dumps(obj))
    elif s is not None:
      k.set_contents_from_string(s)
    else:
      k.set_contents_from_file(fp)
    conn.close()

  def load(self, key, t=None):
    conn = boto.connect_s3(self.access_key, self.secret_key)
    bucket = conn.get_bucket(self.bucket)
    k = Key(bucket)
    k.key = key
    if t is not None and t == 'obj':
      o = pickle.loads(k.get_contents_as_string())
    else:
      o = k.get_contents_as_string()
    conn.close()
    return o

  def list(self):
    conn = boto.connect_s3(self.access_key, self.secret_key)
    bucket = conn.get_bucket(self.bucket)
    for i in bucket.list(): 
      yield i.name
    conn.close()
