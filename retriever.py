import re
import os
import requests
import json
from PartA import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pickle
import math
ranking=dict()
check_docid=[]
N=55393
import merger
def retrieve(query):
    global check_docid
    query = str(query)
    queries=simple_tokenize(query.split())
    rankingfile= open('ranked_index', 'rb')
    for q in queries:
        dict = pickle.load(rankingfile)
        if q ==queries[0]:
            if q in dict.keys():
                #ranking for
                for i in dict[q]:
                    ranking[i[0]]=i[3]
        else:
            for i in dict[q]:
                if i[0] in ranking.keys():
                    ranking[i[0]]+=i[3]

    counter=0
    for k, v in sorted(ranking.items(), key=lambda item: item[1],reverse=True):
        print(get_urls(k))
        counter+=1
        if(counter==5):
            break

def get_urls(word):
    dbfile = open('urls', 'rb')
    results = ""
    while 1:    # Horrible condition, never do this ever ever ever
        try:
            #[[123]],[[456]]
            dict = pickle.load(dbfile)
            if word in dict.keys():
                results=dict[word]
        except(EOFError):
            break
    dbfile.close()
    return results


def get_wordcount(word):
    dbfile = open('words', 'rb')
    results = ""
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            # [[123]],[[456]]
            dict = pickle.load(dbfile)
            if word in dict.keys():
                results=dict[word]
        except(EOFError):
            break
    dbfile.close()
    return results
if __name__ == '__main__':
    print("Please enter the term:")
    term = input().lower()
    retrieve(term)