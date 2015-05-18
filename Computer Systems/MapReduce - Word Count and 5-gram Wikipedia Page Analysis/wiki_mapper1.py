#!/usr/bin/python
import sys
from operator import itemgetter

gram_list = []

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into 3-gram, count, and list of pages
    gram, gram_count, pages = line.split('\t', 2)
    # convert count to integer
    try:
        gram_count = int(gram_count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    gram_list.append([gram, gram_count, pages])

    
#sort the list in reverse order   
gram_list = sorted(gram_list, key=itemgetter(1), reverse=True)
for i in xrange(0,5):
    temp = gram_list[i][2].split('\t')
    #Remove duplicate pages
    tempset = set(temp)
    uniquepages = '\t'.join(tempset)
    # write results with key being count for sorting purposes
    print '%s\t%s\t%s' % (gram_list[i][1], gram_list[i][0], uniquepages)
    
