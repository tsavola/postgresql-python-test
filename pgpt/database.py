client = False

def init():
	global client
	client = True

	with open() as conn:
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
	import postgresql
	return postgresql.open("pq://localhost/")

def call(func):
	if client:
		import pickle

		def dbcall(*args, **kwargs):
			params = pickle.dumps((args, kwargs))

			with open() as db:
				proc = db.proc("pythoncall(text, text, bytea)")
				result = proc(func.__module__, func.__name__, params)

			return pickle.loads(result)

		return dbcall

	return func
