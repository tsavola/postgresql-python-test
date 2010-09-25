client = False

def _open():
	import postgresql
	return postgresql.open("pq://localhost/")

class Database(object):
	def __init__(self):
		self.conn = _open()
		self.proc = self.conn.proc("pythoncall(text, text, bytea)")

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.conn.close()

def init():
	global client
	client = True

	with _open() as conn:
		conn.execute("""
			CREATE OR REPLACE FUNCTION pythoncall (modname text, funcname text, params bytea)
			RETURNS bytea AS $$
				import importlib
				import pickle
				mod = importlib.import_module(modname)
				func = getattr(mod, funcname)
				args, kwargs = pickle.loads(params)
				result = func(*args, **kwargs)
				return pickle.dumps(result)
			$$ LANGUAGE plpython3u""")

def open():
	return Database()

def call(func):
	if client:
		import pickle

		def dbcall(db, *args, **kwargs):
			params = pickle.dumps((args, kwargs))
			result = db.proc(func.__module__, func.__name__, params)
			return pickle.loads(result)

		return dbcall

	return func
