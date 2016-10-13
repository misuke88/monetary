import os
import sys
import jpype
import nltk
import numpy

from settings import DATA_DIR
from konlpy.tag import Twitter
from pprint import pprint
from matplotlib import pylab, font_manager, rc
#from gensim import corpora, models, similarities

pos_tagger = Twitter()
# nltk.download()
font_fname = 'c:/windows/Fonts/Gautami.ttf'
font_name = font_manager.FontProperties(fname = font_fname).get_name()
rc('font', family=font_name)

def read_data(filename):
	with open(filename, 'r') as f:
		data = [line.split('\t') for line in f.read().splitlines()]
		data = data[1:] #  header 제외
	return data

def tokenize(doc):
	return ['/'.join(t) for t in pos_tagger.pos(doc, norm =True, stem = True)]

def term_exists(doc):
	return {'exist({})'.format(word): (word in set(doc)) for word in selected_words}

if __name__ == '__main__':


	# nltk classifier
	train_data = read_data('%s/train.txt' % DATA_DIR)
	test_data = read_data('%s/test.txt' % DATA_DIR)
	train_docs= [(tokenize(row[1]), row[2]) for row in train_data]
	test_docs= [(tokenize(row[1]), row[2]) for row in test_data]
	d_list = []

	# print(train_docs[0][0])
	tokens = [t for d in train_docs for t in d[0]] # num of tokens in train documents
	text = nltk.Text(tokens, name = 'NMSC')
	for d in range(50):
		d_list.append(text.vocab().most_common(50)[d][0])
	tmp_text = [d for d in text if d not in d_list]

	selected_words = [f[0] for f in text.vocab().most_common(500)]
	train_xy = [(term_exists(d),c) for d, c in train_docs]		
	test_xy = [(term_exists(d),c) for d, c in test_docs]		

	# classifier

	classifier = nltk.NaiveBayesClassifier.train(train_xy)
	print(nltk.classify.accuracy(classifier, test_xy))
	classifier.show_most_informative_features(10)
	# print(len(tmp_text)) # number of tokens
	# # print(len(set(text.tokens))) # number of unique tokens
	# pprint(text.vocab().most_common(10)) # frequency distribution
	# text.plot(50)
	# text.collocations()
	# print(len(tokens))
	# pprint(train_docs[0])


	# gensim



# print(len(train_data))
# print(len(test_data))

# print(len(train_data[0]))
# print(len(test_data[0]))

# https://github.com/konlpy/konlpy/issues/71(DLL 에러날때)