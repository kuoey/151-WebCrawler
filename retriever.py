import re
import os
import requests
import json
from PartA import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pickle
import math
from merger import *
ranking=dict()
check_docid=[]
N=55393
import merger
# def retrieve(query):
#     global check_docid
#     query = str(query)
#     queries=simple_tokenize(query.split())
#     rankingfile= open('index', 'rb')
#     for q in queries:
#         dict = pickle.load(rankingfile)
#         if q ==queries[0]:
#             if q in dict.keys():
#                 #ranking for
#                 for i in dict[q]:
#                     ranking[i[0]]=i[3]
#         else:
#             for i in dict[q]:
#                 if i[0] in ranking.keys():
#                     ranking[i[0]]+=i[3]
#
#     counter=0
#     for k, v in sorted(ranking.items(), key=lambda item: item[1],reverse=True):
#         print(get_urls(k))
#         counter+=1
#         if(counter==5):
#             break

def retrever_test(query):
    global check_docid
    query = str(query)
    queries = simple_tokenize(query.split())
    docids=set()
    check_docid=[]
    ranking=dict()
    result=dict()
    N = 55393
    idf = []
    for q in queries:
        postings = search(q)
        idf.append(math.log(N / len(postings)))

        if len(docids)==0:
            docids=  set(i[0] for i in postings)
        else:
            docids &= set(i[0] for i in postings)
        # print("Posting",postings)
        for i in postings:
            if i[0] in docids:

                if i[0] in ranking.keys():
                    if i not in check_docid:
                        # print(ranking[i[0]],((1 + math.log(i[1])),i[2]))
                        ranking[i[0]].append(tuple(map(operator.add, ranking[i[0]][len(ranking[i[0]])-1],((1 + math.log(i[1])),i[2]))))
                    else:
                        ranking[i[0]][len(ranking[i[0]])-1]=tuple(map(operator.add, ranking[i[0]][len(ranking[i[0]])-1],((1 + math.log(i[1])),i[2])))
                else:
                    ranking[i[0]]=[(float(i[1]),i[2])]
                check_docid.append(i[0])
            else:
                if i[0] in ranking.keys():
                    ranking.pop(i[0])
    # print(ranking.keys())
    for i in range(len(idf)):
        for j in ranking.keys():
            result[j]=(ranking[j][i][0]/idf[i])+ranking[j][i][0]
    counter=0
    # print(result)
    # print(idf, ranking,result)
    for k, v in sorted(result.items(), key=lambda item: item[1],reverse=True):
        # print(k)
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
    retrever_test(term)