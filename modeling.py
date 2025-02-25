#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv
import logging

import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
import sklearn

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import linear_model, datasets
from sklearn import metrics
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from pandas import *

from settings import DATA_DIR, LOG_DIR
import utils

TOTAL_INDEX = 'djia gspc ixic'.split() # dow jones. snp500, nasdaq, vol
EXPID = utils.get_expid()
utils.set_logger('%s/%s.log' % (LOG_DIR, EXPID), 'DEBUG')
# TODO: log configurations (ex: parsing method etc) and/or commit id

def openfiles(filename):
    data = pd.read_csv(filename, sep='\t', header = 0)
    data = data.where((pd.notnull(data)), '')   # Replace np.nan with ''
    return data

def preprocessing(X, y):

    idx = y[y['sentiment'] != 'STAY'].index.tolist()
    idx2 = y[y['sentiment'] == 'STAY'].sample(frac=0.2).index.tolist()
    idx.extend(idx2)
    #print(len(idx))
    #idx = np.random.choice(len(y['sentiment']='STAY'), 0.5)
    #idx = np.random.rand(len(y[y['sentiment']=='STAY'])) <0.5
    #idx = y[y['sentiment'] != 'STAY'].index.tolist()
    X = X.loc[idx]
    y = y.loc[idx]
   # X = X[~idx]
   # y = y[~idx]
    #print(len(y))

    return X, y

def tokenizing(docs, mode=None, min_df = 0.03, max_df =0.5):

    if mode=='tf':
        vectorizer = CountVectorizer(min_df = min_df, max_df = max_df)
    elif mode=='tfidf':
        vectorizer = TfidfVectorizer(min_df = min_df, max_df = max_df)
    else:
        raise Exception('Invalid mode %s' % mode)
    logging.info(vectorizer)
    matrix_td = vectorizer.fit_transform(docs) # term doc matrix

    return matrix_td

def generate_LR(X_train, X_test, y_train, y_test):

    logreg = sklearn.preprocessing.LabelEncoder()
    logreg = linear_model.LogisticRegression(C=1e5, class_weight='auto')
    logging.info(logreg)
    model = logreg.fit(X_train, y_train)
    train_predicted = model.predict(X_train)
    test_predicted = model.predict(X_test)
    probs = model.predict_proba(X_test)
    train_accuracy = metrics.accuracy_score(y_train, train_predicted)
    test_accuracy = metrics.accuracy_score(y_test, test_predicted)
    cm = metrics.confusion_matrix(y_test, test_predicted)
    report = metrics.classification_report(y_test, test_predicted)
    return cm, train_accuracy, test_accuracy

def generate_RF(X_train, X_test, y_train, y_test):

    rf = RandomForestClassifier(n_estimators=50, min_samples_leaf=3)
    logging.info(rf)
    rf.fit(X_train, y_train)
    train_predicted = rf.predict(X_train)
    test_predicted = rf.predict(X_test)

    train_accuracy = metrics.accuracy_score(y_train, train_predicted)
    test_accuracy = metrics.accuracy_score(y_test, test_predicted)
    cm = confusion_matrix(y_test, test_predicted)
    return cm, train_accuracy, test_accuracy

def cross_validation_10(X, y):
    lr_scores = cross_val_score(linear_model.LogisticRegression(), X, y, scoring ='accuracy', cv = 10 )
    rf_scores = cross_val_score(RandomForestClassifier(), X.toarray(), y, scoring ='accuracy', cv = 10 )
    logging.info("CV: Accuracy of Logistic Regression is %.4f\n, and Accuracy of Random Forest is %.4f\n." % (lr_scores.mean, rf_scores.mean))

if __name__ == '__main__':

    filenameX = '%s/text_X.txt' % DATA_DIR
    filenameY = '%s/text_Y.txt' % DATA_DIR

    X = openfiles(filenameX)
    y = openfiles(filenameY)
    X, y = preprocessing(X, y)
    ids = X['id']

    #raise Exception('Stop')

    docs = tokenizing(list(X['sentence']), mode='tfidf') # term doc matrix
    logging.info(docs.shape)
    # docX = pd.DataFrame(docs, index=ids).to_sparse().sort_index()
    docX = pd.SparseDataFrame([pd.SparseSeries(docs[i].toarray().ravel()) for i in np.arange(docs.shape[0])],\
            index =ids).sort_index()
    X = docX
    y = y['sentiment'].sort_index()

    logging.info(X.shape)
    X= np.array(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=102)
    logging.info("Modeling of logistic regression...")
    lr_cm, lr_train_accuracy, lr_test_accuracy = generate_LR(X_train, X_test, y_train, y_test) #logistic regression
    logging.info("Accuracy of Logistic Regression\n train: %.4f, test: %.4f\n" % (lr_train_accuracy, lr_test_accuracy))
    logging.info('\n%s' % str(lr_cm))

    logging.info("Modeling of random forest...")
    rf_cm, rf_train_accuracy, rf_test_accuracy = generate_RF(X_train, X_test, y_train, y_test) # #random forest
    logging.info("Accuracy of Random Forest\n  train: %.4f, test: %.4f\n" % (rf_train_accuracy, rf_test_accuracy))
    logging.info('\n%s' % str(rf_cm))
