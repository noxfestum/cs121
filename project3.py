import lxml
from bs4 import BeautifulSoup
import nltk
import re, os
import math
import sys
import string
'''
word = {word:({id: tf-idf }, df:# }
'''

word = {}#'a0':({}, 0, 0),}

def tokenize(path):
    soup = BeautifulSoup(open(path), "lxml")
    s = soup.body.text.encode('utf-8').lower()
    sw = re.sub(r'[^a-z^0-9]', ' ', s)
    #sw = re.sub('['+string.punctuation+']',' ', s)
    tokens = nltk.word_tokenize(sw)
    return tokens

def indexing(path, word):
    tokens = tokenize(path)
    path = path.split('/')[-2] + "/" + path.split('/')[-1]
    for token in tokens:
        if token not in word:
            word[token] = ({path:1}, [1])
        else:
            if path not in word[token][0]:
                word[token][0][path] = 1
                word[token][1][0] += 1
            else:
                word[token][0][path] += 1
    return word


def dfitf(word, n=37497):
    for w in word.keys():
        idf = int(math.log10(n / word[w][1][0]))
        for doc in word[w][0].keys():
            tf = int(1 + math.log10(word[w][0][doc]))
            word[w][0][doc] = tf+idf

def output_data(word):
    file = open('/Users/Archer/Desktop/words.txt', "w")
    for w in word:
        # token - docId1, tf-idf1 ; docId2, tf-idf2
        pass
        
    file.close()

path = '/Users/Archer/Desktop/WEBPAGES_RAW/3/90'

indexing(path,word)
indexing('/Users/Archer/Desktop/WEBPAGES_RAW/3/77', word)
indexing('/Users/Archer/Desktop/WEBPAGES_RAW/3/79', word)

dfitf(word, 37497)
print word

