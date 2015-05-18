#!/usr/bin/python

from operator import itemgetter
import sys

gram_list = []


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
        
    # parse the input we got from mapper.py
    gram_count, gram, pages = line.split('\t', 2)
        
    # convert count (currently a string) to int
    try:
        gram_count = int(gram_count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    #add each 5-gram to the list
    gram_list.append([gram, gram_count, pages])
    
#sort the list in reverse order   
gram_list = sorted(gram_list, key=itemgetter(1), reverse=True)
for i in xrange(0,5):
    temp = gram_list[i][2].split('\t')
    tempset = set(temp)
    uniquepages = '\n'.join(tempset)
    # write results to stdout
    print '%s %s\n%s' % (gram_list[i][0], gram_list[i][1], uniquepages)
    
