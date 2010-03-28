import pickle

obj = pickle.load(open("_lat", "r"))
assert type(obj) == type({})

obj2 = pickle.load(open("__combined", "r"))

assert type(obj2) == type({})

objs = obj
objs.update(obj2)


pickle.dump(objs, open("__combined", "w"))

