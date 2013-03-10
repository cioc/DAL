'''
import DAL
ngrams = DAL.create('ngrams')
print ngrams.subsets()

for gram in ngrams.iter('googlebooks-eng-1M-1gram-20090715-0.csv.zip'):
  print gram
'''
'''
import DAL
sou = DAL.create('sou')

speaches = sou.subsets()

for l in sou.iter(speaches[0]):
  if len(l) > 0:
    print l
'''
'''
import DAL
wishes = DAL.create('wishes')

print wishes.subsets()

def f(i): 
  if 'profile_use_background_image' in i['user'] and i['user']['profile_use_background_image']:
    return True
  else:
    return False

c = 0
for w in wishes.filter('wish-2012-12-01.json', f):
  c += 1

print c

o = []
o.append(wishes.byid(('wish-2012-12-01.json', 0)))
o.append(wishes.byid(('wish-2012-12-01.json', 1)))

wishes.display(o)
'''

from DAL import create
#create a handle to the tinyimages dataset
tinyimages = create('tinyimages')

#load in tinyimages 0 through 99
#x = tinyimages.byid((0, 100))

x = tinyimages.search('cat', 2000)

print x

#display those images
#tinyimages.display(x)
