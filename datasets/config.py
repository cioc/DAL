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
              'AWS_ACCESS_KEY': 'AKIAI2EP4WVCJ2ZIWUEQ',
              'AWS_SECRET_KEY': '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'
            },
            'wishes': {
              'bucket': 'ml-wishes'
            },
            'ngrams': {
              'bucket': 'ml-ngrams'
            },
            'sou': {
              'bucket': 'ml-sou'
            }
          }

def config():
  return _config
