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

punc=['!','"','#','$','%','&','\'',',','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']


indir = sys.argv[1]
hcount=0
scount=0
tcount=0
finaloutput=open('nboutput2.txt','w+')


with open('nbmodel2.txt', 'r') as fp:
    data = json.load(fp)
hamprior = data['priorham']
spamprior = data['priorspam']

def nbcalculations(tcount):
    hprecision = 0.0
    hrecall = 0.0
    hf1 = 0.0
    sprecision = 0.0
    srecall = 0.0
    sf1 = 0.0
    with open('nboutput2.txt','r') as fp:
        data = fp.readlines()

    a1 = 0.0
    b1 = 0.0
    c1 = 0.0
    a2 = 0.0
    b2 = 0.0
    c2 = 0.0
    accuracy=0.0

    for d in data:
        d = d.split(' ')

        #print d[1],d[0]
        if (d[0] == 'HAM') and (re.search('ham', d[1])):
            a1 += 1
        elif (d[0] == 'HAM') and (re.search('spam', d[1])):
            b1 += 1
        elif (d[0] == 'SPAM') and (re.search('ham', d[1])):
            c1 += 1

        if (d[0] == 'SPAM') and (re.search('spam', d[1])):
            a2 += 1
        elif (d[0] == 'SPAM') and (re.search('ham', d[1])):
            b2 += 1
        elif (d[0] == 'HAM') and (re.search('spam', d[1])):
            c2 += 1
    if tcount != 0:
        accuracy = float(a1 + a2) / float(tcount)
    else:
        accuracy = 0

    if (a1 + b1):
        hprecision = float(a1)/float(a1+b1)
    else :
        hprecision= 0
    if (a1 + c1):

        hrecall = float(a1)/float(a1+c1)
    else :
        hrecall=0


    if (a2 + b2):
        sprecision = float(a2)/float(a2+b2)
    else :
        sprecision= 0
    if (a2 + c2):

        srecall = float(a2)/float(a2+c2)
    else :
        srecall=0
    if (hprecision + hrecall):
        hf1 = float((2 * hprecision * hrecall) / float(hprecision + hrecall))
    else:
        hf1 = 0

    if (sprecision + srecall):
        sf1 = float(2 * sprecision * srecall) / (sprecision + srecall)
    else:
        sf1=0


    print "Ham precision:",hprecision
    print "Ham recall:",hrecall
    print "Ham F1 Score: ",hf1
    print "Spam precision:",sprecision
    print "Spam recall:",srecall
    print "Spam F1:",sf1
    print "Accurcy:",accuracy


for root, dirs, filenames in os.walk(indir):
    for f in filenames:

        if (f == ".DS_Store" or f == 'LICENSE' or f == 'README.txt'):
            print " "
        else:
            tcount += 1
            with open(os.path.join(root, f),'r') as r:
                word = r.read()
                word = re.sub("\d+", "", word)
                word=word.lower()
                for z in range(0, len(punc)):
                    if punc[z] in word:

                        if punc[z] != '\'':
                            word = word.replace(punc[z], " ")
                        else:
                            word = word.replace(punc[z], "")

                word= word.split()

                hp = -2.0
                sp = -2.0

                for w in word:
                    if w not in data:
                        continue

                    else:

                        hp = hp + hamprior + math.log(data[w]['ham'], 2)
                        sp = sp + spamprior +  math.log(data[w]['spam'], 2)

                if (max(hp, sp) == hp):
                    hcount += 1
                    #print "ham file" , f
                    finaloutput.write("HAM ")


                else:
                    scount += 1
                    #print "spam file", f
                    finaloutput.write("SPAM ")


                finaloutput.write(f + "\n")
    nbcalculations(tcount)

print "Total document count:",tcount
print "Total  classified Spam files:",scount
print "Total classified Ham files:",hcount






