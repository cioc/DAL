import json
import os
import os.path
import getpass
from os.path import expanduser

def get_config_file():
  home = expanduser("~")
  if os.path.exists(home+'/.dalconfig' % (username)):
    return open(home+'/.dalconfig' % (username), 'r')
  elif os.path.exists(home+'/dalconfig.json' % (username)):
    return open(home+'/dalconfig.json' % (username), 'r')
  else:
    return None

def config():
  f = get_config_file()
  if f is not None:
    o = json.loads(f.read())
    f.close()
    return o
  else:
    raise Exception('No DAL config file detected')

def local():
  f = get_config_file()
  if f is not None:
    o = json.loads(f.read())
    f.close()
    if 'system' in o and 'local' in o['system']:
      return o['system']['local']
    return False
  else:
    raise Exception('No DAL config file detected') 
