from datasets.tinyimages import TinyImage

class_table = {'tinyimages': TinyImage}

def create(name):
  if name in class_table:
    return class_table[name]()
  else:
    raise Exception("No Such Dataset with name: %s" % (name))
