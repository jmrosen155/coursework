from pyspark import SparkContext

import sys

from pyspark.mllib.feature import IDF
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.clustering import KMeans

import numpy as np
from collections import Counter

def checkpages(x):
    pagedata = x.split('\t')
    page = pagedata[0]
    words = pagedata[1]
    words = words.split(' ')
    return (page, words)
    
def getindex(x, htf):
    temp = []
    for word in x:
        temp.append(htf.indexOf(word))
    return temp

def matchclusters(pages, clusters, t):
    page_words = Counter(pages)
    cluster_assign = []
    for i in xrange(0, len(clusters)):
        cluster_words = clusters[i]
        sum1 = 0
        for word in cluster_words:
            sum1 = sum1 + page_words[word]
        if sum1 > t:
            cluster_assign.append(i)
    return cluster_assign


sc = SparkContext(appName="Part2")
lines = sc.textFile(sys.argv[1])

pages = lines.map(lambda x: checkpages(x))
pageinfo = pages.map(lambda x: x[0])
pageinfo_list = pageinfo.collect()
words = pages.map(lambda x: x[1])

words_all = words.flatMap(lambda x: x).distinct()
words_all = words_all.collect()

htf = HashingTF(75000)
tf = htf.transform(words)

idf = IDF().fit(tf) #compute the IDF vector
tfidf = idf.transform(tf) #scale the term frequencies by IDF

words_indices = words.map(lambda x: getindex(x, htf))

# Create dictionary of hash id to word
indexes = {}
for word in words_all:
    if htf.indexOf(word) in indexes.keys():
        indexes[htf.indexOf(word)].append(word)
    else:
        indexes[htf.indexOf(word)] = [word]

num_clusters = 50

clusters = KMeans.train(tfidf, k=num_clusters, maxIterations=10, runs=3, initializationMode="random")
centers = clusters.centers

topic_indices = []
for i in xrange(0, num_clusters):
    temp = list(np.argsort(centers[i])[::-1][0:100])
    topic_indices.append(temp)

t = int(sys.argv[4])
page_assign_RDD = words_indices.map(lambda x: matchclusters(x, topic_indices, t))
page_assign = page_assign_RDD.collect()


page_dict = {}
for i in xrange(0, len(page_assign)):
    page_dict[i] = page_assign[i]

cluster_dict = {}
for i in xrange(0, len(page_assign)):
    temp = page_dict[i]
    for cluster in temp:
        if cluster in cluster_dict.keys():
            cluster_dict[cluster].append(i)
        else:
            cluster_dict[cluster] = [i]

output = []
output1 = []
for i in xrange(0, len(cluster_dict)):
    if len(cluster_dict[i]) < 50 and len(cluster_dict[i]) > 1:
        topics = topic_indices[i][0:5]
        topics_all = topic_indices[i]
        topics_final = []
        topics_final_all = []
        for topic in topics:
            for word in indexes[topic]:
                topics_final.append(word.encode('utf-8'))
        for topic in topics_all:
            for word in indexes[topic]:
                topics_final_all.append(word.encode('utf-8'))
        titles = []
        title_indices = cluster_dict[i]
        for index in title_indices:
            temp1 = pageinfo_list[index]
            temp1 = temp1.split(' ', 1)[1]
            titles.append(temp1.encode('utf-8'))
        temp2 = str(topics_final) + ', ' + str(titles)
        output.append(temp2)
        for topic1 in topics_final_all:
                for title1 in titles:
                    output1.append(str(topic1) + ' ' + str(title1)) 

    
textFile = open(sys.argv[2], 'w')

for item in output:
    textFile.write(item + '\n')

textFile.close()

textFile = open(sys.argv[3], 'w') 
#textFile = open('output/p3_output.txt', 'w') 
for item in output1:
    textFile.write(item + '\n')    
textFile.close()

sc.stop()