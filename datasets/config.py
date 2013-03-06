'''
Stores configuration for all datasets
'''

_config = {'tinyimages': { 
              'metapath': "/tiny/tinyimages/tiny_metadata.bin",
              'datapath': "/tiny/tinyimages/tiny_images.bin"
            },
            'cache': {
              'path': '/mnt',
              'size': '10G',
              'AWS_ACCESS_KEY': 'KEY_HERE',
              'AWS_SECRET_KEY': 'KEy_HERE'
            },
            'wishes': {
              'bucket': 'ml-wishes'
            },
          }

def config():
  return _config
