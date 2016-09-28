########################################################
# real test 

# load data
install.packages("regex")
install.packages("RTextTools")
install.packages("e1071")
library(regex)
library(RTextTools)
library(e1071)

Sys.setlo
setwd("D:/text analysis/MonetaryPolicy/MonetaryPolicy_Text/")
setpath = "D:/text analysis/MonetaryPolicy/MonetaryPolicy_Text/"
up = read.csv("./INFO_CLASS.csv", header = TRUE)
obs = dim(up)[1]


# filename = paste("D:/text analysis/MonetaryPolicy/MonetaryPolicy_Text/",gsub("[[:space:]]","",up[1,1], fixed= TRUE), ".txt",)
# delete blank lines

raw =""
x <- "[брд╖-]" 
for (i in 1:obs){
  filename = paste(setpath,up[i,1], ".txt", sep="")
  con = file(filename, open ="r")
  tmptext = readLines(con)
  # delete blank lines
  texts= tmptext[sapply(tmptext, nchar)>0]
  for (text in texts){
    #text = gsub("бр", "",text) 
    #text=gsub(x, "", gsub("[[:punct:]]", "", substring(text, 2, nchar(text))))
    text=gsub(x, "", gsub("[[:punct:]]", "", text))
    raw = rbind(raw, cbind(text, up[i,2]))
  }
}
mat= create_matrix(raw, language="korean", 
                   removeStopwords=FALSE, removeNumbers=TRUE, 
                   stemWords=FALSE, tm::weightTfIdf)

mat= create_matrix(raw, removeStopwords=FALSE, removeNumbers=TRUE, stemWords=FALSE, tm::weightTfIdf)
mat$dimnames$Terms
