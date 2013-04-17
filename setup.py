from distutils.core import setup
setup(name='DAL',
      version='1.0',
      description='Data Access Layer (DAL) Library for lsdacluster',
      author='Charles Cary',
      author_email='cioc@uchicago.edu',
      url='http://github.com/cioc/DAL',
      packages=['DAL', 'DAL.datasets', 'DAL.hadoop'])
