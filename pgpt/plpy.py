from . import database as __database
if not __database.client:
	from plpy import *
del __database
