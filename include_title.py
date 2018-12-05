import lxml
from bs4 import BeautifulSoup
import nltk
import re, os
import math
import string
import json
from collections import OrderedDict
from operator import itemgetter
'''
word = {word:({id: tf-idf }, df:# )}
'''

DEBUG = False

word = {} # word:({id: [tf-idf, header = 0/ 1]}, [df])#
url_dict = {} # docID: url

def load_url_dict():
    '''loads bookkeeping.json and returns resulted json dict'''
    # file_path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/bookkeeping.json'
    file_path = '/Users/Archer/Desktop/WEBPAGES_RAW/bookkeeping.json'
    json_text = open(file_path).read()
    return json.loads(json_text)

def load_index():
    '''loads saved index to word if file exists, otherwise indexes all documents'''
    try:
        file = open('/Users/Archer/Desktop/words.txt', 'r')
        for line in file:
            item = line.split(" - ")
            word[item[0]] = ({}, [1])
            docs = item[1].split("; ")
            for doc in docs:
                doc_item = doc.split(',')
                docID = doc_item[0][4:]
                word[item[0]][0][docID][0] = int(doc_item[1])
                word[item[0]][0][docID][1] = int(doc_item[2])
        file.close()
    # equivalent to FileNotFoundError
    except IOError:
        index_all(url_dict,word)
        tfidf(word, 37497)

def find_url(doc):
    '''returns url according to the docID'''
    return url_dict[doc]

def tokenize(path):
    '''returns a list of tokens in each document(pass by path)'''
    tokens = []
    hs = []
    soup = BeautifulSoup(open(path), "lxml")
    if soup.body != None:
        s = soup.body.text.encode('utf-8').lower()
        sw = re.sub(r'[^a-z^0-9]', ' ', s)
        #sw = re.sub('['+string.punctuation+']',' ', s)
        tokens = nltk.word_tokenize(sw)

        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for header in headers:
            h = header.text.encode('utf-8').lower()
            h = re.sub(r'[^a-z^0-9]', ' ', h)
            for i in nltk.word_tokenize(h): hs.append(i)

    return tokens, hs


def indexing(path, word):
    '''indexing a single document and storing to database '''
    tokens, headers = tokenize(path)
    path = path.split('/')[-2] + "/" + path.split('/')[-1]
    for token in tokens:
        if token not in word:
            word[token] = ({path:[1, 0]}, [1])
        else:
            if path not in word[token][0]:
                word[token][0][path] = [1, 0]
                word[token][1][0] += 1
            else:
                word[token][0][path][0] += 1
        if DEBUG == True:
            print token, word[token], '\n'
    print(path)
    for token in headers:

        word[token][0][path][1] = 1

def index_all(url_dict, word):
    '''indexes all documents'''
    # base_path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/'
    base_path = '/Users/Archer/Desktop/WEBPAGES_RAW/'
    for doc in url_dict:
        doc_path = base_path + doc
        indexing(doc_path, word)

def tfidf(word, n=37497):
    '''calculate tf-idf for all index word'''
    for w in word.keys():
        idf = int(math.log10(n / word[w][1][0]))
        for doc in word[w][0].keys():
            tf = int(1 + math.log10(word[w][0][doc]))
            word[w][0][doc] = tf*idf

'''
def search(w): #w= sys.argv[1]
    # print url contains given word w
    w = w.lower()
    title = '/Users/Archer/Desktop/'+ w+'.txt'
    # title = '/Users/Mescetina/Downloads/'+ w+'.txt'
    file = open(title, "w")
    docs = word[w][0].keys()
    for doc in docs:
        file.write(find_url(doc)+'\n')
    file.close()
    #return result
'''

def search(w):
    '''print url contains given word w'''
    query = w.strip().lower().split()
    ranked_docs = {}
    for i in query:
        for doc in word[i][0]:
            if doc not in ranked_docs:
                ranked_docs[doc] = word[i][0][doc][0]
            else:
                ranked_docs[doc] += word[i][0][doc][0]

            if word[i][0][doc][1] == 1:
                ranked_docs[doc] += 2

    '''Sorted docs by score in descending order'''
    ranked_docs = OrderedDict(sorted(ranked_docs.items(), key=itemgetter(1), reverse = True))

    for doc in ranked_docs:
        print ranked_docs[doc], find_url(doc)
        # Only print the docs with score higher than 3 to check the top results
        #if ranked_docs[doc] <= 3:
        #    break


def output_data(word):
    '''write index into txt file on desktop'''
    # file = open('/Users/Mescetina/Downloads/words.txt', 'w')
    file = open('/Users/Archer/Desktop/words.txt', "w")
    for w in word:
        docs =[]
        for doc in word[w][0]:
            docs.append('doc_'+doc+','+ str(word[w][0][doc][0])+','+ str(word[w][0][doc][1]))
        wordlog = "; ".join(docs)
        file.write(w + " - " + wordlog +"\n")
    file.close()

def read_input():
    while True:
        user_input = raw_input("Search: (press ctrl-D to exit) ")
        # python 2 use raw_input() instead of python 3 use input()
        search(user_input)

if __name__ == '__main__':
    url_dict = load_url_dict()
    load_index()
    output_data(word)
    read_input()

    #search("computer science")

