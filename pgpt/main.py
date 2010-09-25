import os

from . import database
database.init()

from . import test

def main():
	print("client:", os.getpid())
	print("db:", test.getpid())
	print("db:", test.getpid())
	print("version:", test.version())

if __name__ == "__main__":
	main()
