import os
import sys
import jpype

from settings import DATA_DIR
from konlpy.tag import Twitter
from pprint import pprint

pos_tagger = Twitter()

def read_data(filename):
	with open(filename, 'r') as f:
		data = [line.split('\t') for line in f.read().splitlines()]
		data = data[1:] #  header 제외
	return data

def tokenize(doc):
	return ['/'.join(t) for t in pos_tagger.pos(doc, norm =True, stem = True)]

if __name__ == '__main__':

	train_data = read_data('%s/train.txt' % DATA_DIR)
	test_data = read_data('%s/test.txt' % DATA_DIR)
	train_docs= [(tokenize(row[1]), row[2]) for row in train_data]
	test_docs= [(tokenize(row[1]), row[2]) for row in test_data]

	pprint(train_docs[0])
# print(len(train_data))
# print(len(test_data))

# print(len(train_data[0]))
# print(len(test_data[0]))

# https://github.com/konlpy/konlpy/issues/71(DLL 에러날때)