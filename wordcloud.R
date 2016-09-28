
install.packages("KoNLP")
install.packages("RColorBrewer")
library(KoNLP)
library(wordcloud)
library(RColorBrewer)

## read files

f = file("C:/Users/infomax/Documents/MonetaryPolicy/MonetaryPolicy_Text/201002.txt", blocking = F)
txtLines = readLines(f)
txtLines
## extract nouns and save noun-count pair table
nouns = sapply(txtLines, extractNoun, USE.NAMES = F)
wordcount = table(unlist(nouns))

pal = brewer.pal(9, "Set1")
wordcloud(names(wordcount),freq=wordcount, scale=c(5,1),rot.per=0.25,min.freq=2, random.order=F,random.color=T,colors=pal)
