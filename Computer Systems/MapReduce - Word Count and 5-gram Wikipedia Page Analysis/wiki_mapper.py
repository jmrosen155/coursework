#!/usr/bin/python
import sys
import xml.etree.ElementTree as ET

# input comes from STDIN (standard input)
string = ''
for line in sys.stdin:
    #Create string of each page
    if '<page>' in line:
        string = line
    elif '</page>' not in line:
        string = string + line
    else:
        string = string + line
        string = '<data>\n'+string+'\n</data>'
        #Extract title, id, and text of the page
        root = ET.fromstring(string)
        page = root.find('page')
        name = page.find('title').text
        name = name.encode('ascii', 'ignore')
        pageid = page.find('id').text
        revision = page.find('revision')
        text = revision.find('text').text
        #Ensure text is not None
        if not text:
            text = ''
        
        for line in text.splitlines():    
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
            words_temp = []
            # remove words that contain non-ascii characters
            for i in xrange(0, len(words)):
                if all(ord(char) < 128 for char in words[i]):
                    words_temp.append(words[i])
            words = words_temp
                    
            # make sure the line has at least 5 words
            if len(words) > 4:
                for i in xrange(0, len(words)-4):
                    gram = ' '.join(words[i:i+5])
                    # write the results to STDOUT (standard output);
                    # what we output here will be the input for the
                    # Reduce step, i.e. the input for reducer.py
                    #
                    # tab-delimited; the trivial word count is 1
                    print '%s\t%s\t%s\t%s' % (gram, 1, name, pageid)
                
        string = ''
            
    