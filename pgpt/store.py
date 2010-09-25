from . import database
from . import plpy

if database.client:
	import postgresql

	with database.open() as db:
		try:
			db.execute("""
				CREATE TABLE store (
					name serial NOT NULL PRIMARY KEY,
					data hstore NOT NULL
				)""")
		except postgresql.exceptions.DuplicateTableError:
			pass

class Store(object):
	def __init__(self, name):
		self.name = name

	def __setitem__(self, key, value):
		_store_set(self.name, key, value)

	def __getitem__(self, key):
		return _store_get(self.name, key)

	def __delitem__(self, key):
		_store_del(self.name, key)

	def drop(self):
		_store_drop(self.name)

@database.call
def make_store():
	for row in plpy.execute("INSERT INTO store (data) VALUES (''::hstore) RETURNING name"):
		return Store(row["name"])

@database.call
def get_store(name):
	plan = plpy.prepare("SELECT EXISTS (SELECT 1 FROM store WHERE name = $1)", ["integer"])
	for row in plpy.execute(plan, [name]):
		return Store(name)

@database.call
def _store_set(name, key, value):
	plan = plpy.prepare("UPDATE store SET data = data || hstore($2, $3) WHERE name = $1",
	                    ["integer", "text", "text"])
	plpy.execute(plan, [name, key, value])

@database.call
def _store_get(name, key):
	plan = plpy.prepare("SELECT data -> $2 AS value FROM store WHERE name = $1",
	                    ["integer", "text"])
	for row in plpy.execute(plan, [name, key]):
		return row["value"]

@database.call
def _store_del(name, key):
	plan = plpy.prepare("SELECT data - $2 FROM store WHERE name = $1",
	                    ["integer", "text"])
	plpy.execute(plan, [name, key])

@database.call
def _store_drop(name):
	plan = plpy.prepare("DELETE FROM store WHERE name = $1", ["integer"])
	plpy.execute(plan, [name])
