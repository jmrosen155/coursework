#!/usr/bin/python
import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip().lower()
    # remove double, triple, and quadruple hyphens
    line = line.replace('----',' ')
    line = line.replace('---',' ')
    line = line.replace('--',' ')
    # remove hyphens surrounded by spaces
    line = line.replace(' -',' ')
    line = line.replace('- ',' ')
    # keep only letters, hyphens, and spaces
    line = ''.join([char for char in line if char.isalpha() or char == '-' or char==' '])
    # split the line into words
    words = line.split()
    # make sure the line has at least 3 words
    if len(words) > 2:
        for i in xrange(0, len(words)-2):
            gram = ' '.join(words[i:i+3])
            # write the results to STDOUT (standard output);
            # what we output here will be the input for the
            # Reduce step, i.e. the input for reducer.py
            #
            # tab-delimited; the trivial word count is 1
            print '%s\t%s' % (gram, 1)
