import urllib2
import urllib
import json
import config

class MapReduce:
  def __init__(self):
    self.config = config.config()
    self.aws_access_key=self.config['cache']['AWS_ACCESS_KEY'] 
    self.aws_secret_key=self.config['cache']['AWS_SECRET_KEY']
    self.hardware = {'1node': 1, '5node': 2}
  
  def runjob(self, hardware, jobfile):
    try:
      data = urllib.urlencode([('aws_access_key', self.aws_access_key),('aws_secret_key', self.aws_secret_key),('job_script', jobfile),('hardware', self.hardware[hardware])])   
      req = urllib2.urlopen('http://lsda.cs.uchicago.edu/hadoop', data)
      o = json.loads(req.read())
      return o['output']
    except urllib2.HTTPError as e:
      return ('err', e.fp.read())

  def jobs(self):
    try:
      data = urllib.urlencode([('aws_access_key', self.aws_access_key),('aws_secret_key', self.aws_secret_key)])
      req = urllib2.urlopen('http://lsda.cs.uchicago.edu/hadoop?'+data)
      o = json.loads(req.read())
      return o['result']
    except urllib2.HTTPError as e:
      return ('err', e.fp.read())

  def status(self, jobflowid):
    try:
      data = urllib.urlencode([('aws_access_key', self.aws_access_key),('aws_secret_key', self.aws_secret_key)])
      req = urllib2.urlopen('http://lsda.cs.uchicago.edu/hadoop/'+jobflowid+'?'+data)
      o = json.loads(req.read())
      return o['status']
    except urllib2.HTTPError as e:
      return ('err', e.fp.read())


