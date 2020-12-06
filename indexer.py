import re
import os
import requests
import json
from PartA import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pickle

inverted_list = dict()  # key= token, values = list(Posting)
docid_n = 0
dump_counter = 0
bigBook = {}
token_num = set()
urls={}
# total_words={}


# class Posting(object):
#
#     def __init__(self, docid, tfidf, fields, pos):
#         """
#         Construct a new 'Posting' object.
#         :param docid: Doc id, a int
#         :param tfidf: Frequency count or TF-IDF
#         :param fields: Fields, not in use yet
#         :param pos: Positions, not in use yet
#         :return: returns nothing
#         """
#         self.docid = docid
#         self.tfidf = tfidf
#         self.fields = fields
#         self.pos = pos

def posting(docid, freq,important,tf_idf):
    return [docid, freq,important,tf_idf]


def build_index(document):
    """
    Storing inverted_list as indexer.
    :param document: a json file.
    :return: returns nothing
    """

    global bigBook
    global dump_counter
    global docid_n
    docid_n += 1
    dump_counter += 1
    with open(document,encoding = "utf-8")as f:
        data = json.load(f)
        # print(data["content"])
        urls[docid_n]=data["url"]
        # total_words[docid_n]=len(data["content"])

    soup = BeautifulSoup(data["content"], 'html.parser')
    # print(soup.prettify())
    # print(soup.find_all('h1'))
    # print(soup.find_all('h3'))
    # s = soup.get_text()
    for type in ['body','h1','h2','h3','strong','b']:
        print(type)
        # s= soup.find_all(type)
        # print(s)
        for s in soup.find_all(type):
            wordList = simple_tokenize(s.text.split())
            bigBook = combineFreq(wordList, bigBook)
            b_sorted = sorted(bigBook.items(), reverse=True,
                              key=operator.itemgetter(1))
            for token, freq in b_sorted:
                token_num.add(token)
                if token not in inverted_list.keys():
                    # print(token, freq)
                    inverted_list[token] = list()
                t=0
                if type =='body':
                    t=0
                if type =='h1':
                    t=4
                if type =='h2':
                    t=3
                if type =='h3':
                    t=2
                if type =='b' or type=='strong':
                    t=1
                inverted_list[token].append(posting(docid_n, freq, t, 0))
                # print(inverted_list[token])

            bigBook.clear()

    if dump_counter == 12000:
        print("dump")
        # writing pickle
        dbfile = open("index", 'ab')
        pickle.dump(inverted_list, dbfile)
        dbfile.close()
        inverted_list.clear()
        urlfile = open("urls", 'ab')
        pickle.dump(urls, urlfile)
        urlfile.close()
        urls.clear()
        # wordsfile = open("words", 'ab')
        # pickle.dump(total_words, wordsfile)
        # wordsfile.close()
        # total_words.clear()
    f.close()
    print(docid_n, document, len(token_num))


if __name__ == '__main__':
    """
    For M1 testing purpose
    """
    if os.path.exists("output.txt"):  # Resets the output file
        os.remove("output.txt")

    print("Enter directory:")
    directory = input()
    for root, dirs, files in os.walk(directory, topdown=True):
        print(root)

        for file in files:
            if file.endswith('.json'):
                build_index(os.path.join(root, file))

            else:
                print(file)

    if len(inverted_list) != 0:
        dbfile = open('index', 'ab')
        pickle.dump(inverted_list, dbfile)
        inverted_list.clear()
        dbfile.close()
        urlfile = open("urls", 'ab')
        pickle.dump(urls, urlfile)
        urlfile.close()
        # wordsfile = open("words", 'ab')
        # pickle.dump(total_words, wordsfile)
        # wordsfile.close()
    totalfile= open('total','ab')
    pickle.dump(docid_n,totalfile)
    totalfile.close()

    print(len(token_num))
