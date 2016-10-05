import csv
import numpy as np
import pandas as pd
from settings import DATA_DIR
from nltk.corpus import wordnet as wn

#def openfiles(filename, arg):

#def read_files(filename):

def write_table(data, filename):
    data.to_csv(filename, sep='\t', header=True, index = False)

def split_train_test(data):
	idx = np.random.rand(len(data)) <0.8
	train = data[idx]
	test = data[~idx]
	return train, test

i =0 

if __name__ == '__main__':
	
	filename= '%s/INFO_CLASS.csv' % DATA_DIR
	wfilename = '%s/textfile.txt' % DATA_DIR
	trainfilename = '%s/train.txt' % DATA_DIR
	testfilename = '%s/test.txt' % DATA_DIR
	data = pd.read_csv(filename, sep=",", header= 0)
	data = pd.DataFrame(data)
	columns = ['id', 'sentence', 'sentiment']
	testfile = pd.DataFrame(columns = columns)
	ids = []
	sentence = []
	sentiment = []
	delchar = [',','-', '□','o','  ']
	# txtname = "%s/%s.txt" % (DATA_DIR, data['FILENAME'][0])
	j = 0 
	for i in range(len(data['FILENAME'])-1):
		txtname = "%s/%s.txt" % (DATA_DIR, data['FILENAME'][i])
		with open(txtname, 'r') as f:
			lines = filter(None, f.read().split("\n"))
			for line in lines:
				j = j +1
				for ch in delchar:
					line = line.replace(ch, '')	
				ids.append(j)
				sentence.append(line)
				sentiment.append(data['CLASS'][i])
	testfile['id'] = ids
	testfile['sentence'] = sentence
	testfile['sentiment'] = sentiment
	# write_table(testfile, wfilename)
	train, test = split_train_test(testfile)
	write_table(train, trainfilename)
	write_table(test, testfilename)
	
	# print(len(train),len(test))
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
