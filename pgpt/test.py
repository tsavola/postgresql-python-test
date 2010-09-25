from . import database
from . import store

def main():
	storename = local()
	remote(storename)

def local():
	s = store.make_store()
	s["key1"] = "value1"
	s["key2"] = "value2"
	del s["key1"]
	return s.name

@database.call
def remote(storename):
	s = store.get_store(storename)
	assert s["key2"] == "value2"
	s.drop()
