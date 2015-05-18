#!/usr/bin/python

from operator import itemgetter
import sys

number = 0
list = []


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
        
    # parse the input we got from mapper.py
    gram_count, gram = line.split('\t', 1)
        
    # convert count (currently a string) to int
    try:
        gram_count = int(gram_count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    #add each 3-gram to the list
    list.append([gram, gram_count])
    
#sort the list in reverse order   
list = sorted(list, key=itemgetter(1), reverse=True)
for i in xrange(0,10):
    print '%s %s' % (list[i][0], list[i][1])