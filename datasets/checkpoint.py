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
     
  def store(self, key, obj):
    conn = boto.connect_s3(self.access_key, self.secret_key)
    bucket = conn.get_bucket(self.bucket)
    k = Key(bucket)
    k.key = key
    k.set_contents_from_string(pickle.dumps(obj))
    conn.close()

  def load(self, key):
    conn = boto.connect_s3(self.access_key, self.secret_key)
    bucket = conn.get_bucket(self.bucket)
    k = Key(bucket)
    k.key = key
    o = pickle.loads(k.get_contents_as_string())
    conn.close()
    return o

  def list(self):
    conn = boto.connect_s3(self.access_key, self.secret_key)
    bucket = conn.get_bucket(self.bucket)
    o = bucket.list() 
    conn.close()
    return o
