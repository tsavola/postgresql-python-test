from . import database
from . import store

def main():
	s = store.make_store()
	name = local(s)
	value = remote(s.name)
	print(value)

def local(s):
	s["key1"] = "value1"
	s["key2"] = "value2"
	del s["key1"]

@database.call
def remote(name):
	s = store.get_store(name)
	value = s["key2"]
	s.drop()
	return value
