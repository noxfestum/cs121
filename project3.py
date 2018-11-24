import lxml
from bs4 import BeautifulSoup
import nltk
import re, os
import math
import sys
import string
import json
'''
word = {word:({id: tf-idf }, df:# )}
'''

DEBUG = False

word = {} # word:({id: tf-idf }, df:#
url_dict = {} # docID: url

def load_url_dict():
    '''loads bookkeeping.json and returns resulted json dict'''
    file_path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/bookkeeping.json'
    json_text = open(file_path).read()
    return json.loads(json_text)

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
        if DEBUG == True:
            print token, word[token], '\n'

def index_all(url_dict, word):
    '''indexes all documents'''
    base_path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/'
    for doc in url_dict:
        doc_path = base_path + doc
        indexing(doc_path, word)

def tfidf(word, n=37497):
    '''calculate tf- idf for all index word'''
    for w in word.keys():
        idf = int(math.log10(n / word[w][1][0]))
        for doc in word[w][0].keys():
            tf = int(1 + math.log10(word[w][0][doc]))
            word[w][0][doc] = tf+idf


def search(w): #w= sys.argv[1]
    '''print url contains given word w'''
    docs = word[w][0].keys()
    #result = []
    for doc in docs:
        print(find_url(doc))
        #result.append(find_url(doc))
    #return result

def output_data(word):
    '''write index into txt file on desktop'''
    file = open('/Users/Archer/Desktop/words.txt', "w")
    for w in word:
        docs =[]
        for doc in word[w][0]:
            docs.append('doc_'+doc+','+ str(word[w][0][doc]))
        wordlog = "; ".join(docs)
        file.write(w + " - " + wordlog +"\n")
    file.close()




url_dict = load_url_dict()
index_all(url_dict,word)
tfidf(word, 37497)
output_data(word)

path = '/Users/Archer/Desktop/WEBPAGES_RAW/3/90'
path = '/Users/Mescetina/Downloads/WEBPAGES_RAW/3/90'
indexing(path,word)
indexing('/Users/Archer/Desktop/WEBPAGES_RAW/3/77', word)
indexing('/Users/Archer/Desktop/WEBPAGES_RAW/3/79', word)

# for w in word:
#     print w, word[w]
