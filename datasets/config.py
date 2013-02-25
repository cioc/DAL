'''
Stores configuration for all datasets
'''

_config = {'tinyimages': { \
              'metapath': "/tiny/tinyimages/tiny_metadata.bin",\
              'datapath': "/tiny/tinyimages/tiny_images.bin"\
            },\
            'cache': {\
              'path': '/tmp',\
              'size': '10G'\
            }\
          }

def config():
  return _config
