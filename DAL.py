from datasets.tinyimages import TinyImage
from datasets.wishes import Wishes
from datasets.sou import Sou
from datasets.ngrams import Ngrams
from datasets.crime import Crime

class_table = {'tinyimages': TinyImage,
               'wishes': Wishes,
               'sou': Sou,
               'ngrams': Ngrams,
               'crime': Crime}

def create(name):
  if name in class_table:
    return class_table[name]()
  else:
    raise Exception("No Such Dataset with name: %s" % (name))
