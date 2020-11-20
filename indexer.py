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
total_words={}

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

def posting(docid, tfidf):
    return [docid, tfidf]


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
    with open(document)as f:
        data = json.load(f)
        # print(data["content"])
        urls[docid_n]=data["url"]
        total_words[docid_n]=len(data["content"])

    soup = BeautifulSoup(data["content"], 'html.parser')

    s = soup.get_text()

    wordList = simple_tokenize(s.split())
    bigBook = combineFreq(wordList, bigBook)
    b_sorted = sorted(bigBook.items(), reverse=True,
                      key=operator.itemgetter(1))
    for token, freq in b_sorted:
        token_num.add(token)
        if token not in inverted_list.keys():
            # print(token, freq)
            inverted_list[token] = list()
        inverted_list[token].append(posting(docid_n, freq))

    bigBook.clear()
    inverted_list.clear()

    # dbfile = open('index', 'ab')
    # pickle.dump(inverted_list, dbfile)
    # dump_counter=0
    # inverted_list.clear()
    # dbfile.close()
    # f.close()

    # pickle stuffs
    # Its important to use binary mode
    # dbfile = open("index", 'ab')
    #
    # # source, destination
    # pickle.dump(inverted_list, dbfile)
    # dbfile.close()
    # dbfile now contains the pickled version of inverted list

    # loading data from pickle / reading pickle


    # fileOUT = open("index.txt", "a")
    if dump_counter == 12000:
        print("dump")
        # writing pickle
        dbfile = open("index", 'ab')
        pickle.dump(inverted_list, dbfile)
        dbfile.close()
        urlfile = open("urls", 'ab')
        pickle.dump(urls, urlfile)
        urlfile.close()
        wordsfile = open("words", 'ab')
        pickle.dump(total_words, wordsfile)
        wordsfile.close()
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
    print(len(token_num))
