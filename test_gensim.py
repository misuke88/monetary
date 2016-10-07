from settings import DATA_DIR
from gensim import corpora, models, similarities
from gensim.models import doc2vec
from collections import namedtuple

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
	tagged_train_docs = [TaggedDocument(d, [c]) for d, c in train_docs]
	tagged_test_docs = [TaggedDocument(d, [c]) for d, c in test_docs]

	doc_vectorizer = doc2vec. Doc2Vec(size=300, alpha= 0.025, min_alpha=0.025, seed = 1234)
	doc_vectorizer.build_vocab(tagged_train_docs)

	#Train documnet vectors! gensim 이 안깔려!!!
	for epoch in range(10):
		doc_vectorizer.train(tagged_train_docs)
		doc_vectorizer.alpha -=0.002
		doc_vectorizer.min_alpha = doc_vectorizer.alpha