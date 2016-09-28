import csv
import pandas as pd
from settings import DATA_DIR

#def openfiles(filename, arg):

#def read_files(filename):


if __name__ == '__main__':
	filename= '%s/INFO_CLASS.csv' % DATA_DIR
	
	with open(filename, 'r') as f:
		for line in f.readlines():
			print(line)
