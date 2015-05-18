from pyspark import SparkContext

import sys

from operator import itemgetter

from pyspark.mllib.feature import IDF
from pyspark.mllib.feature import HashingTF

def checkpages(x):
    pagedata = x.split('\t')
    page = pagedata[0]
    words = pagedata[1]
    words = words.split(' ')
    return (page, words)
    
def maxtfidf(x, indexes):
    keys = x.indices
    values = x.values
    keyvals = []
    for i in xrange(0, len(keys)):
        keyvals.append([keys[i], values[i]])
    keyvals = sorted(keyvals, key=itemgetter(1), reverse=True)
    indicator = 0
    index = 0
    while indicator == 0:
        if keyvals[index][0] in indexes.keys():
            words = indexes[keyvals[index][0]]
            words = ' '.join(words)
            output = (words, keyvals[index][1])
            indicator = 1
        else:
            index = index + 1
    return output

sc = SparkContext(appName="Part1")
lines = sc.textFile(sys.argv[1])

pages = lines.map(lambda x: checkpages(x))
pageinfo = pages.map(lambda x: x[0])
pageinfo_list = pageinfo.collect()
words = pages.map(lambda x: x[1])

htf = HashingTF()
tf = htf.transform(words)

idf = IDF().fit(tf) #compute the IDF vector
tfidf = idf.transform(tf) #scale the term frequencies by IDF

# Create dictionary of hash id to word
words_all = words.flatMap(lambda x: x)
words_all = list(set(words_all.collect()))
indexes = {}
for word in words_all:
    if htf.indexOf(word) in indexes.keys():
        indexes[htf.indexOf(word)].append(word)
    else:
        indexes[htf.indexOf(word)] = [word]


tfidf_mapping = tfidf.map(lambda x: maxtfidf(x, indexes))

tfidf_list = tfidf_mapping.collect()

output = []

for i in xrange(0, len(pageinfo_list)):
    output.append(pageinfo_list[i] + ' ' + tfidf_list[i][0] + ' ' + str(tfidf_list[i][1]))
    
textFile = open(sys.argv[2], 'w')

for item in output:
    textFile.write(item + '\n')

textFile.close()

sc.stop()


