from pyspark import SparkContext

import sys

import xml.etree.ElementTree as ET

import math

import re

from operator import itemgetter

if len(sys.argv) < 2:
    print ('Please provide the location of the input file')
    exit(-1)
    

def checkpages(x):
    root = ET.fromstring(x.encode('utf-8'))
    if root.find('ns').text == '0':
        name = root.find('title').text
        name = name.encode('ascii', 'ignore')
        pageid = root.find('id').text
        revision = root.find('revision')
        text = revision.find('text').text
        if not text:
            return
        else:
            text = text.lower()
            # keep only letters, hyphens, and spaces
            #text = text.translate(None, '`~!@#$%^&*()_+=[{]}:;"\',<.>/?\|')
            text = re.sub('[' + re.escape('0123456789`~!@#$%^&*()_+=[{]}:;"\',<.>/?\|') + ']', '', text)
            # remove double, triple, and quadruple hyphens
            text = text.replace('----',' ')
            text = text.replace('---',' ')
            text = text.replace('--',' ')
            # remove hyphens surrounded by spaces
            text = text.replace(' -',' ')
            text = text.replace('- ',' ')
            # split the line into words
            words = text.split()
            words_temp = []
            # remove words that contain non-ascii characters
            for i in xrange(0, len(words)):
                if all(ord(char) < 128 for char in words[i]):
                    words_temp.append(words[i])
            words = words_temp
            text = ' '.join(words)
            text = text.encode('ascii', 'ignore')
            page_info = pageid + ' ' + name  
            return (page_info, text)
    else:
        return


def countwords(x):
    words = x[1].split()
    uniques = set(words)
    freqs = [(word, words.count(word)) for word in uniques]
    return (x[0], freqs)
    
def wordcontained(x):
    words = x[1].split()
    uniques = set(words)
    freqs = [(word, 1) for word in uniques]
    return (x[0], freqs)

def calcTFIDF(x, IDF_dict):
    sum = 0
    score = []
    for i in xrange(0,len(x[1])):
        sum = sum + x[1][i][1]
    for i in xrange(0,len(x[1])):
        temp = IDF_dict[x[1][i][0]]
        score.append((x[1][i][0], temp * (float(x[1][i][1])/sum)))
    max_score = max(score, key=itemgetter(1))
    return (x[0], max_score)



   
sc = SparkContext(appName="Part1")
lines = sc.textFile(sys.argv[1])
pages = lines.map(lambda x: checkpages(x))
total_docs = pages.count()

wordcount_page = pages.map(lambda x: countwords(x))

wordcount_all = pages.map(lambda x: wordcontained(x))
wordcount_all = wordcount_all.flatMap(lambda x: x[1])
IDF = wordcount_all.reduceByKey(lambda a, b: a + b)
IDF = IDF.map(lambda x: (x[0], math.log(total_docs/float(x[1]))))
IDF_list = IDF.collect()
IDF_dict = dict(IDF_list)


TFIDF = wordcount_page.map(lambda x: calcTFIDF(x, IDF_dict))

output = TFIDF.collect()

for i in xrange(0,len(output)):
    output[i] = output[i][0] + ' ' + output[i][1][0] + ' ' + str(output[i][1][1])

#output.saveAsTextFile(sys.argv[2])

textFile = open('output/p1_output.txt', 'w')

for item in output:
    textFile.write(item + '\n')

textFile.close()

sc.stop()