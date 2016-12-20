#! /usr/bin/python
# -*- coding: utf-8 -*-

from codecs import open
from konlpy.tag import Twitter
import csv
import numpy as np
import pandas as pd
from settings import DATA_DIR
from nltk.corpus import wordnet as wn

ENCODING = 'euckr'

def write_table(data, filename):
    data.to_csv(filename, sep='\t', header=True, index = False, encoding='utf8')

def tagging(line):
    stoptag = ['Josa', 'Puctuation', 'Number']
    line_tag = t.pos(line, norm=True, stem =True)
    line = ' '.join(['/'.join(q) for q in line_tag if q[1] not in stoptag])

    #newline =[]
    #for i, l in enumerate(line_tag):
    #    if i< len(line_tag)-1:
    #        newline.append('%s%s' % (line_tag[i], line_tag[i+1]))
    #newline= ' '.join([q for q in newline])

    #line = '%s %s' % (line, newline.encode('utf8'))
    return line.strip()

def textgram(line, flag):

    flaggram =[]

    for i in range(len(line.split(' '))-1):
        seg = [line[i], line[i+1]]
        flaggram.append(''.join(seg))
    flaggram = ' '.join([q for q in flaggram])
    #newline = ' '.join([''.join(q[i-1], q[i]) for i, q in enumerate(line, start=1)])
    line = '%s %s' % (line, flaggram)
    return line

def split_train_test(data):
    idx = np.random.rand(len(data)) <0.8
    train = data[idx]
    test = data[~idx]
    return train, test

if __name__ == '__main__':

    t= Twitter()
    filename= '%s/INFO_CLASS.csv' % DATA_DIR
    #wfilename = '%s/data_tagging.txt' % DATA_DIR

    data = pd.read_csv(filename, sep=",", header= 0, encoding='utf-8')
    data = pd.DataFrame(data)
    columns = ['id', 'sentence', 'sentiment']
    testfile = pd.DataFrame(columns = columns)
    ids=[]
    sentence = []
    sentiment = []
    delchar = ["  ", "-", u"□", '" ', u'o']
    j = 0
    i =0
    flag = 1
    for i in range(len(data['FILENAME'])-1):
        txtname = "%s/%s.txt" % (DATA_DIR, data['FILENAME'][i])
        with open(txtname, 'r', encoding=ENCODING) as f:
            lines = [line.replace('\t', ' ').strip() for line in f.read().split("\n")]
            lines = filter(None, lines)
            for line in lines:
                j = j +1
                for ch in delchar:
                    line = line.replace(ch, '')
                line = tagging(line.strip())
                ids.append(j)
                sentiment.append(data['CLASS'][i])
                sentence.append(line)

    testfile['id'] = ids
    testfile['sentence'] = sentence
    testfile['sentiment'] = sentiment

    wfilename = '%s/stem_data_tagging_%s_gram.txt' % (DATA_DIR, flag)
    write_table(testfile, wfilename)
