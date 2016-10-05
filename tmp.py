import os
import sys

from nltk.corpus import wordnet as wn
from settings import DATA_DIR

def read_data(filename):
	with open(filename, 'r') as f:
		data = [line.split('\t') for line in f.read().splitlines()]
		data = data[1:] #  header 제외
	return data

if __name__ == '__main__':
	
	train_data = read_data('%s/train.txt' % DATA_DIR)
	test_data = read_data('%s/test.txt' % DATA_DIR)

# print(len(train_data))
# print(len(test_data))

# print(len(train_data[0]))
# print(len(test_data[0]))