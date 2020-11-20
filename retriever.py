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

def retrieve(query):
    query = str(query)
    queries = query.split()
    print(queries)
    openDBfile = open("index", 'rb')
    db = pickle.load(openDBfile)
    openURLfile = open("urls", 'rb')
    url = pickle.load(openURLfile)
    openWfile = open("words", 'rb')
    total_words = pickle.load(openWfile)
    # db holds the inverted list that was put into dbfile
    N=len(db.keys())
    for q in queries:
        if q in db.keys():
            print("IN",q)
            for status in db[q]:
                print("Status",status)
                q_docid= status[0]
                q_freq= status[1]

                tf = q_freq / total_words[q_docid]
                idf = math.log(N/ len(db[q]))
                tf_idf= tf * idf
                print("TF_IDF",tf_idf)
                if q_docid not in ranking.keys():
                    ranking[q_docid]=tf_idf
                else:
                    ranking[q_docid]+=tf_idf

    counter=0

    for k, v in sorted(ranking.items(), key=lambda item: item[1]):
        print(url[k])
        counter+=1
        if(counter==5):
            break
    openURLfile.close()
    openDBfile.close()
    openWfile.close()
if __name__ == '__main__':
    retrieve("cristina lopes")