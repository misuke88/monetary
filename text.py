import csv
import pandas as pd
from settings import DATA_DIR

#def openfiles(filename, arg):

#def read_files(filename):

i =0 

if __name__ == '__main__':
	filename= '%s/INFO_CLASS.csv' % DATA_DIR
	data = pd.read_csv(filename, sep=",", header= 0)
	print(data)
	for i in range(len(data)-1):
		txtname = "%s.txt" % data[i][0]
		with open(txtname, 'r') as f:
			for line in f.readlines():
				testfile.add(line)
	print(len(data))
	# with open(filename, 'r') as f:
	# 	for line in f.readlines():
	# 		print(len(line))
	# 		i = i + 1
			#print(line,i)
	#len(filenames)
