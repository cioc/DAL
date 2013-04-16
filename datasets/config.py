import json

'''
Loads configuration for all datasets
'''

def config():
  f = open('/home/charles_user/dalconfig.json', 'r')
  o = json.loads(f.read())
  f.close()
  return o

def local():
  f = open('/home/charles_user/dalconfig.json', 'r')
  o = json.loads(f.read())
  f.close()
  if 'system' in o and 'local' in o['system']:
    return o['system']['local']
  return False

