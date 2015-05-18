from pyspark import SparkContext

import sys

import xml.etree.ElementTree as ET

import math

import re

from operator import itemgetter

from operator import add

from collections import Counter

if len(sys.argv) < 5:
    print ('Please provide the location of the 2 input files and the similarity threshold')
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
    

# command line args: page dataset, threshold, page links, iterations
   
sc = SparkContext(appName="Part3")
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


shortest_page = []
for comp in components:
    min_page = comp[0]
    min_count = words_per_page[comp[0]]
    for page in comp:
        if (words_per_page[page] < min_count):
            min_page = page
            min_count = words_per_page[page]
    shortest_page.append(min_page)


  
shortest_page = [page.split(' ', 1) for page in shortest_page]



def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls, shortest_page):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    if (parts[0] in [x[0] for x in shortest_page]) and (parts[1] in [x[0] for x in shortest_page]):
        p1 = [x[0] for x in shortest_page].index(parts[0])
        p1 = shortest_page[p1]
        p1 = ' '.join(p1)
        p2 = [x[0] for x in shortest_page].index(parts[1])
        p2 = shortest_page[p2] 
        p2 = ' '.join(p2)
        return p1, p2
    else:
        return


# Loads in input file of page links
lines = sc.textFile(sys.argv[3])

# Loads all URLs from input file and initialize their neighbors.
links = lines.map(lambda urls: parseNeighbors(urls, shortest_page))
links = links.filter(lambda x: x != None)
links = links.distinct().groupByKey().cache()

# Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
ranks = links.map(lambda (url, neighbors): (url, 1.0))

# Calculates and updates URL ranks continuously using PageRank algorithm.
for iteration in xrange(int(sys.argv[4])):
    # Calculates URL contributions to the rank of other URLs.
    contribs = links.join(ranks).flatMap(
        lambda (url, (urls, rank)): computeContribs(urls, rank))

    # Re-calculates URL ranks based on neighbor contributions.
    ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)



ranks_list = ranks.collect()

ranks_list = sorted(ranks_list, key=itemgetter(1), reverse = True)

textFile = open('output/p3_output.txt', 'w')

# Collects all URL ranks and dump them to console.
for i in xrange(0, 10):
    textFile.write(ranks_list[i][0] + ' ' + str(ranks_list[i][1]) + '\n')


textFile.close()

sc.stop()




