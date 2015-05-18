from pyspark import SparkContext

import sys

import xml.etree.ElementTree as ET

import math

import re

from operator import itemgetter

from collections import Counter

if len(sys.argv) < 3:
    print ('Please provide the location of the input file and similarity threshold')
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
    #max_score = max(score, key=itemgetter(1))
    return (x[0], score)


# Less efficient version
'''
def calcSim(x, TFIDF_list, threshold):
    page1 = x[0]
    words1 = x[1]
    words1_dict = dict(words1)
    index = [y[0] for y in TFIDF_list].index(x[0]) + 1
    sim_list = [page1]
    for i in xrange(index, len(TFIDF_list)):
        page2 = TFIDF_list[i][0]
        words2 = dict(TFIDF_list[i][1])
        score = 0
        for j in xrange(0, len(words1)):
            if words1[j][0] in words2.keys():
                temp = (words1[j][1] - words2[words1[j][0]])**2
            else:
                temp = words1[j][1]**2
            score = score + temp
        for j in xrange(0, len(TFIDF_list[i][1])):
            if TFIDF_list[i][1][j][0] not in words1_dict.keys():
                temp = TFIDF_list[i][1][j][1]**2
                score = score + temp
        score = score ** 0.5
        if score < threshold:
            sim_list.append(page2)
    return (sim_list)
'''

# More efficient version
def calcSim(x, TFIDF_list, threshold):
    page1 = x[0]
    index = [y[0] for y in TFIDF_list].index(page1) + 1
    words1_dict = TFIDF_list[index-1][1]
    sim_list = [page1]
    for i in xrange(index, len(TFIDF_list)):
        page2 = TFIDF_list[i][0]        
        score = 0
        temp = words1_dict.copy()
        temp.subtract(TFIDF_list[i][1])
        for key in temp:
            temp[key] = temp[key]**2
        score = sum(temp.values())**0.5
        if score < threshold:
            sim_list.append(page2)
    return (sim_list)
        
            

   
sc = SparkContext(appName="Part2")
lines = sc.textFile(sys.argv[1])
threshold = float(sys.argv[2])
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

TFIDF_list = TFIDF.collect()
TFIDF_listdict = []

for page in TFIDF_list:
    TFIDF_listdict.append((page[0], Counter(dict(page[1]))))

similarity = TFIDF.map(lambda x: calcSim(x, TFIDF_listdict, threshold))

sim_list = similarity.collect()

components = []
while len(sim_list) > 0:
    first, rest = sim_list[0], sim_list[1:]
    first = set(first)
    lf = -1
    while len(first) > lf:
        lf = len(first)
        rest2 = []
        for r in rest:
            if len(first.intersection(set(r))) > 0:
                first |= set(r)
            else:
                rest2.append(r)     
        rest = rest2
    components.append(list(first))
    sim_list = rest


words_per_page = dict(pages.map(lambda x: (x[0], len(x[1].split()))).collect())

output = []
output.append(str(len(components)))
for comp in components:
    min_page = comp[0]
    min_count = words_per_page[comp[0]]
    for page in comp:
        if (words_per_page[page] < min_count):
            min_page = page
            min_count = words_per_page[page]
    output.append(min_page + ' ' + str(len(comp)))


textFile = open('output/p2_output.txt', 'w')

for item in output:
    textFile.write(item + '\n')

textFile.close()

sc.stop()

