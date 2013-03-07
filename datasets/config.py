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
              'AWS_ACCESS_KEY': '...KEY...HERE...',
              'AWS_SECRET_KEY': '...KEY...HERE...'
            },
            'wishes': {
              'bucket': 'ml-wishes'
            },
            'sou': {
              'bucket': 'ml-sou'
            }
          }

def config():
  return _config
