import lxml
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import re, os
import math
import string
import json
from collections import OrderedDict
from operator import itemgetter
'''
word = {word:({id: tf-idf }, [df:# ])}
'''

DEBUG = False

word = {} # word:({id: tf-idf }, [df:#])
url_dict = {} # docID: url
stop_words = set(stopwords.words('english'))


def load_url_dict():
    '''loads bookkeeping.json and returns resulted json dict'''
    file_path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/bookkeeping.json'
    # file_path = '/Users/Archer/Desktop/WEBPAGES_RAW/bookkeeping.json'
    json_text = open(file_path).read()
    return json.loads(json_text)

def load_index():
    '''loads saved index to word if file exists, otherwise indexes all documents'''
    try:
        file = open('/Users/Mescetina/Downloads/words.txt', 'r')
        for line in file:
            item = line.split(" - ")
            word[item[0]] = ({}, [1])
            docs = item[1].split("; ")
            for doc in docs:
                doc_item = doc.split(',')
                docID = doc_item[0][4:]
                word[item[0]][0][docID] = int(doc_item[1])
        file.close()
    # equivalent to FileNotFoundError
    except IOError:
        index_all(url_dict,word)
        tfidf(word, 37497)

def find_url(doc):
    '''returns url according to the docID'''
    return url_dict[doc]

def tokenize(path):
    tokens = []
    soup = BeautifulSoup(open(path), "lxml")
    if soup.body != None:
        s = soup.body.text.encode('utf-8').lower()
        sw = re.sub(r'[^a-z^0-9]', ' ', s)
        #sw = re.sub('['+string.punctuation+']',' ', s)
        tokens = []
        for t in nltk.word_tokenize(sw):
            if t not in stop_words:
                tokens.append(t)
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
    if DEBUG == True:
        print path

def index_all(url_dict, word):
    '''indexes all documents'''
    base_path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/'
    # base_path = '/Users/Archer/Desktop/WEBPAGES_RAW/'
    for doc in url_dict:
        doc_path = base_path + doc
        indexing(doc_path, word)

def tfidf(word, n=37497):
    '''calculate tf- idf for all index word'''
    for w in word.keys():
        idf = int(math.log10(n / word[w][1][0]))
        for doc in word[w][0].keys():
            tf = int(1 + math.log10(word[w][0][doc]))
            word[w][0][doc] = tf*idf

def search(w):
    '''print url contains given word w'''
    sw = re.sub(r'[^a-z^0-9]', ' ', w)
    query = nltk.word_tokenize(sw)
    ranked_docs = {}
    for i in query:
        if i in word:
            for doc in word[i][0]:
                if doc not in ranked_docs:
                    ranked_docs[doc] = word[i][0][doc]
                else:
                    ranked_docs[doc] += word[i][0][doc]

    '''Sorted docs by score in descending order'''
    ranked_docs = OrderedDict(sorted(ranked_docs.items(), key=itemgetter(1), reverse = True))

    result_url = []
    for doc in ranked_docs.keys()[:20]:
        result_url.append(find_url(doc))
    return result_url


def output_data(word):
    '''write index into txt file on desktop'''
    file = open('/Users/Mescetina/Downloads/words.txt', 'w')
    # file = open('/Users/Archer/Desktop/words.txt', "w")
    for w in word:
        docs =[]
        for doc in word[w][0]:
            docs.append('doc_'+doc+','+ str(word[w][0][doc]))
        wordlog = "; ".join(docs)
        file.write(w + " - " + wordlog +"\n")
    file.close()

def read_input():
    while True:
        user_input = raw_input("Search (press ctrl-D to exit): ")
        # python 2 use raw_input() instead of python 3 use input()
        for result in search(user_input):
            print result
        print

if __name__ == '__main__':
    url_dict = load_url_dict()
    load_index()
    output_data(word)
    read_input()
