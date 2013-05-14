from datasets.tinyimages import TinyImages
from datasets.wishes import Wishes
from datasets.sou import Sou
from datasets.ngrams import Ngrams
from datasets.crime import Crime
from datasets.cache import Cache
from datasets.rcv1 import rcv1
from datasets.lightcurves import LightCurves
from datasets.wisheslabelled import WishesLabelled

class_table = {'tinyimages': TinyImages,
               'wishes': Wishes,
               'sou': Sou,
               'ngrams': Ngrams,
               'crime': Crime,
               'rcv1': rcv1,
               'wishes-labelled': WishesLabelled,
               'lightcurves': LightCurves}

def create(name):
  if name in class_table:
    return class_table[name]()
  else:
    raise Exception("No Such Dataset with name: %s" % (name))

def cleancache():
  c = Cache()
  c.cleancache()
