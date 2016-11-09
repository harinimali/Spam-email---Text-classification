from __future__ import division

import re
from collections import defaultdict
import os
import sys
import json
import io


d={}
s={}
h={}
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
             'so','than','too','very','can','will','just','don','should','now','s')


indir = sys.argv[1]

ham_count=0
spam_count=0

dict_count = 0



condProb ={}

spam_prob=0.0
ham_prob=0.0


def clean(word):
    word = word.lower()
    if (len(word) < 2):
        return None
    elif (word.isdigit()):
        return None
    elif (word in wordstoremove):
        return None

    return word


def list_to_dict(l):
    #d = defaultdict(int)
    for word in l:
        if word in d:
            d[word] += 1
        else:
            d[word]=1

def spam_to_dict(l):
    #d = defaultdict(int)
    for word in l:
        if word in s:
            s[word] += 1
        else:
            s[word]=1

def ham_to_dict(l):
    #d = defaultdict(int)
    for word in l:
        if word in h:
            h[word] += 1
        else:
            h[word]=1

def text_list(text):
    words = map(clean, re.split('\W+', text.strip()))
    return filter(lambda word: word and (len(word) > 0),words)

def bayes(dict_count,spam_count,ham_count,d,s,h):

    spam_prob = float(float( spam_count)/float(dict_count))
    print spam_prob

    ham_prob = float(ham_count) / float(dict_count)
    print ham_prob
    #print s.keys()
    for word in d.keys():
        #print word,s[word]
        temp = {}
        if word in s.keys():
            spam_temp = s[word]
        else:
            spam_temp = 0

        if word in h.keys():
            ham_temp = h[word]
        else:
            ham_temp = 0

        temp['spam'] = float(spam_temp + 1) / (spam_count + dict_count)
        temp['ham'] = float(ham_temp + 1) / (ham_count + dict_count)
        condProb[word] = temp

    condProb['priorham']=ham_prob
    condProb['priorspam']=spam_prob

    #print condProb





for root, dirs, filenames in os.walk(indir):

    for f in filenames:

        if (f == ".DS_Store" or f == 'LICENSE' or f == 'README.txt'):
            print " "
        else:


            with open(os.path.join(root, f),'r') as r:
                book = r.read()
                word = text_list(book)

                list_to_dict(word)

            dict_count = len(d)

            if f.find("ham")==-1:
                with open(os.path.join(root, f), 'r') as r:
                    a = r.read()
                    spamwords=text_list(a)
                    spam_to_dict(spamwords)
                spam_count = len(s)


            elif f.find("spam")==-1:
                with open(os.path.join(root, f), 'r') as r:
                    b = r.read()
                    hamwords = text_list(b)
                    ham_to_dict(hamwords)
                ham_count = len(h)

bayes(dict_count, spam_count, ham_count, d, s, h)

with open('nbmodel2.txt', 'w+') as fp:
    json.dump(condProb, fp)

