#Parametric memoization via pickling, uses same concept as all of the other memoization decorators
#Serialization is *persistent* throughout the project

import pickle, glob

def ls(filename, dir):
    return dir+"\\"+filename in glob.glob(dir+'/*')

class memoize(object):
    def __init__(self, func):
        self.func = func
        self.name = func.func_name
        if ls(self.name, "memoize"):
            _f = open("memoize/"+self.name, "r")
            self.cache = pickle.load(_f)
            _f.close()
        else:
            self.cache = {}
    def __call__(self, *args):
        try:
            obj = self.cache[args]
            if not obj: self.cache[None]
            #if isinstance(obj, str): self.cache[None]
            return obj
        except KeyError:
            self.cache[args]=value=self.func(*args)
            _f = open("memoize/"+self.name,"w")
            pickle.dump(self.cache, _f)
            _f.close()
            return value
        except TypeError:
            return self.func(*args)
        
