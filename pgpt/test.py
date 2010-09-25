from . import database
from . import store

def main():
	s = store.make_store()
	print(test(s))
	print(dbtest(s))
	s.drop()

def test(s):
	s["key1"] = "value1"
	v = s["key1"]
	del s["key1"]
	return v

@database.call
def dbtest(s):
	return test(s)
