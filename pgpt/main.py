import os

from . import database
database.init()

from . import test

def main():
	test.main()

if __name__ == "__main__":
	main()
