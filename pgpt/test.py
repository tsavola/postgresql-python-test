import os

from . import database
from . import plpy

@database.call
def getpid():
	return os.getpid()

@database.call
def version():
	for row in plpy.execute("SELECT version()"):
		return row["version"]
