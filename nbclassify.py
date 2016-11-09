from __future__ import division

import re
from collections import defaultdict
import os
import sys
import json
import io
import math

wordstoremove = ('i','me','my','myself','we','our','ours','ourselves','you','your','yours',
             'yourself','yourselves','he','him','his','himself','she','her','hers','herself',
             'it','its','itself','they','them','their','theirs','themselves','what','which',
             'who','whom','this','that','these','those','am','is','are','was','were','be','been',
             'being','have','has','had','having','do','does','did','doing','a','an','the','and',
             'but','if','or','because','as','until','while','of','at','by','for','with','about',
             'against','between','into','through','during','before','after','above','below','to',
             'from','up','down','in','out','on','off','over','under','again','further','then',
             'once','here','there','when','where','why','how','all','any','both','each','few',
             'more','most','other','some','such','no','nor','not','only','own','same',
             'so','than','too','very','can','will','just','don','should','now','s','may')

def cleaning(word):
    word = word.lower()
    if (len(word) < 2):
        return None
    elif (word.isdigit()):
        return None
    elif (word in wordstoremove):
        return None

    return word
def convertolist(text):
    clean_words = map(cleaning, re.split('\W+', text.strip()))
    return filter(lambda word: word and (len(word) > 0), clean_words)

indir = sys.argv[1]

finaloutput=open('nboutput.txt','w+')

with open('nbmodel.txt', 'r') as fp:
    data = json.load(fp)
hamprior = data['priorham']
spamprior = data['priorspam']

for root, dirs, filenames in os.walk(indir):
    for f in filenames:

        if (f == ".DS_Store" or f == 'LICENSE' or f == 'README.txt'):
            print " "
        else:

            with open(os.path.join(root, f),'r') as r:
                book = r.read()
                word = convertolist(book)

                hp = -2.0
                sp = -2.0

                for w in word:
                    if w not in data:
                        continue

                    else:

                        hp = hp + hamprior + math.log(data[w]['ham'], 2)
                        sp = sp + spamprior +  math.log(data[w]['spam'], 2)

                if (max(hp, sp) == hp):
                    #print "ham file" , f
                    finaloutput.write("HAM ")

                else:
                    #print "spam file", f
                    finaloutput.write("SPAM ")
                finaloutput.write(f + "\n")






