import csv
import pandas as pd
from settings import DATA_DIR

#def openfiles(filename, arg):

#def read_files(filename):

def write_table(data, filename):
    data.to_csv(filename, sep='\t', header=True)

i =0 

if __name__ == '__main__':
	
	filename= '%s/INFO_CLASS.csv' % DATA_DIR
	wfilename = '%s/textfile.csv' % DATA_DIR
	data = pd.read_csv(filename, sep=",", header= 0)
	data = pd.DataFrame(data)
	columns = ['sentence', 'sentiment']
	testfile = pd.DataFrame(columns = columns)
	sentence = []
	sentiment = []
	delchar = [',','-', '□','o','  ']
	# txtname = "%s/%s.txt" % (DATA_DIR, data['FILENAME'][0])
	for i in range(len(data['FILENAME'])-1):
		txtname = "%s/%s.txt" % (DATA_DIR, data['FILENAME'][i])
		with open(txtname, 'r') as f:
			lines = filter(None, f.read().split("\n"))
			for line in lines:
				for ch in delchar:
					line = line.replace(ch, '')	
				sentence.append(line)
				sentiment.append(data['CLASS'][i])
	testfile['sentence'] = sentence
	testfile['sentiment'] = sentiment
	write_table(testfile, wfilename)

	# print(testfile)
				# docs = filter(None, f.read().split("<DOCUMENT>"))'o'
			# 	# print(len(data))
	# print(len(data['FILENAME']))
	# print(data['FILENAME'][1])

	# testfile = pd.DataFrame(columns = columns)

	#a = data[1][1]
	
	#print(a)

	# for i in range(len(data)-1):
	# 	txtname = "%s.txt" % data[i][0]
	# 	with open(txtname, 'r') as f:
	# 		for line in f.readlines():
	# 			print(line)
				# testfile['sentence'].append(line[])
				# print(len(data))
	# with open(filename, 'r') as f:
	# 	for line in f.readlines():
	# 		print(len(line))
	# 		i = i + 1
			#print(line,i)
	#len(filenames)
