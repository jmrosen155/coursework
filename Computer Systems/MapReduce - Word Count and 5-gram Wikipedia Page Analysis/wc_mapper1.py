#!/usr/bin/python
import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into 3-gram and count
    gram, gram_count = line.split('\t', 1)
    # convert count to integer
    gram_count = int(gram_count)
    # write results with key being count for sorting purposes
    print '%s\t%s' % (gram_count, gram)