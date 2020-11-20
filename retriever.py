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
import merger
def retrieve(query):
    global check_docid
    query = str(query)

    queries=simple_tokenize(query.split())
    # print(queries)
    # openDBfile = open("index", 'rb')
    # db = pickle.load(openDBfile)
    # openURLfile = open("urls", 'rb')
    # url = pickle.load(openURLfile)
    # openWfile = open("words", 'rb')
    # total_words = pickle.load(openWfile)
    # db holds the inverted list that was put into dbfile
    N=55393

    for q in queries:
        inverted_list = merger.get_results(q)
        # print("Inverted_list",inverted_list)

        if inverted_list!=[]:
            temp=list()
            for status in inverted_list:
                # print("Status",status)
                q_docid= status[0]
                q_freq= status[1]
                # if q!=queries[0]:
                #     if q_docid in check_docid:
                #         temp.append(q_docid)
                #         tf = q_freq / get_wordcount(q_docid)
                #         idf = math.log(N / len(inverted_list))
                #         tf_idf = tf * idf
                #         # print("TF_IDF", tf_idf)
                #         if q_docid not in ranking.keys():
                #             ranking[q_docid] = tf_idf
                #         else:
                #             ranking[q_docid] += tf_idf
                #     else:
                #         pass
                # else:
                check_docid.append(q_docid)
                tf = q_freq / get_wordcount(q_docid)
                idf = math.log(N / len(inverted_list))
                tf_idf= tf * idf
                # print("TF_IDF",tf_idf)
                if q_docid not in ranking.keys():
                    ranking[q_docid]=tf_idf
                else:
                    ranking[q_docid]+=tf_idf

                # if len(temp)<len(check_docid):
                #     check_docid=temp
        # print("Check", check_docid)
    counter=0
    rank={}
    # print(ranking)
    for i in check_docid:
        if i not in rank:
            rank[i]=ranking[i]
    ranking.clear()
    # print("Rank:",rank)
    for k, v in sorted(rank.items(), key=lambda item: item[1],reverse=True):
        print(get_urls(k))
        counter+=1
        if(counter==5):
            break
    # openURLfile.close()
    # openDBfile.close()
    # openWfile.close()
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