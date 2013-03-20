import urllib2
import urllib
import json

class MapReduce:
  def __init__(self):
    self.aws_access_key='ACCESS_KEY' 
    self.aws_secret_key='SECRET_KEY'
    self.hardware = {'1node': 1, '5node': 2}
  
  def runjob(self, hardware, jobfile):
    data = urllib.urlencode([('aws_access_key', self.aws_access_key),('aws_secret_key', self.aws_secret_key),('job_script', jobfile),('hardware', self.hardware[hardware])])   
    req = urllib2.urlopen('http://lsda.cs.uchicago.edu/hadoop', data)
    o = json.loads(req.read())
    return o['output']

  def jobstatus(self, jobflowid):
    pass

  def myjobs(self):
    pass

