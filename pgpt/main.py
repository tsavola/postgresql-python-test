import os

def main():
	os.system("bin/psql -c \"select pythoncall('pgpt.test', 'func', 'jeejee')\"")

if __name__ == "__main__":
	main()
