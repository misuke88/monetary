########################################################################################
# "Sentiment analysis with machine learning"
# Under the hood, RTextTools uses the e1071 package which is a R wrapper around libsvm;
#######################################################################################
install.packages("RTextTools")
install.packages("e1071")
library(RTextTools)
library(e1071)

####
# TMS.R is a rJava wrapping of the Korean Morphlogical Analyzer from Saltlux Inc.
####
pos_tweets =  rbind(
  c('I love this car', 'positive'),
  c('This view is amazing', 'positive'),
  c('I feel great this morning', 'positive'),
  c('I am so excited about the concert', 'positive'),
  c('He is my best friend', 'positive')
)


neg_tweets = rbind(
  c('I do not like this car', 'negative'),
  c('This view is horrible', 'negative'),
  c('I feel tired this morning', 'negative'),
  c('I am not looking forward to the concert', 'negative'),
  c('He is my enemy', 'negative')
)

test_tweets = rbind(
  c('feel happy this morning', 'positive'),
  c('larry friend', 'positive'),
  c('not like that man', 'negative'),
  c('house not great', 'negative'),
  c('your song annoying', 'negative')
)

tweets = rbind(pos_tweets, neg_tweets, test_tweets)

# build dtm -> using e1071 library
matrix= create_matrix(tweets[,1], language="english", 
                      removeStopwords=FALSE, removeNumbers=TRUE,  # we can also removeSparseTerms
                      stemWords=FALSE) 

#train the model
mat = as.matrix(matrix)
classifier = naiveBayes(mat[1:10,], as.factor(tweets[1:10,2]))

#test the validity
predicted = predict(classifier, mat[11:15,]); predicted
table(tweets[11:15, 2], predicted)
recall_accuracy(tweets[11:15, 2], predicted)

# using RTextTools library

# build the data to specify response variable, training set, testing set.
container = create_container(matrix, as.numeric(as.factor(tweets[,2])),
                             trainSize=1:10, testSize=11:15,virgin=FALSE)
models = train_models(container, algorithms=c("MAXENT", "SVM", "RF", "BAGGING", "TREE" ))
results = classify_models(container, models)

# accuracy table
table(as.numeric(as.factor(tweets[11:15, 2])), results[,"FORESTS_LABEL"])
table(as.numeric(as.factor(tweets[11:15, 2])), results[,"MAXENTROPY_LABEL"])

# recall accuracy
recall_accuracy(as.numeric(as.factor(tweets[11:15, 2])), results[,"FORESTS_LABEL"])
recall_accuracy(as.numeric(as.factor(tweets[11:15, 2])), results[,"MAXENTROPY_LABEL"])
recall_accuracy(as.numeric(as.factor(tweets[11:15, 2])), results[,"TREE_LABEL"])
recall_accuracy(as.numeric(as.factor(tweets[11:15, 2])), results[,"BAGGING_LABEL"])
recall_accuracy(as.numeric(as.factor(tweets[11:15, 2])), results[,"SVM_LABEL"])

#model summary
analytics = create_analytics(container, results)
summary(analytics)
head(analytics@document_summary)
analytics@ensemble_summary

# To cross validate the results:
N=4
set.seed(2014)
cross_validate(container,N,"MAXENT")
cross_validate(container,N,"TREE")
cross_validate(container,N,"SVM")
cross_validate(container,N,"RF")

# for this work, the "MAXENT" is the best result like naive Bayes. because we only have small data set. 



########################################################
# real test 

# load data

setwd("D:/text analysis/MonetaryPolicy/MonetaryPolicy_Text/")
