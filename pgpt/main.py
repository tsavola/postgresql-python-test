import os

from . import database
database.init()

from . import test

def main():
	print("client:", os.getpid())

	with database.open() as db:
		print("db-1:", test.getpid(db))

		with database.open() as db2:
			print("db-2:", test.getpid(db2))

		print("version:", test.version(db))

if __name__ == "__main__":
	main()
