import re
import os
import requests
import json
from PartA import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup

inverted_list = dict()  # key= token, values = list(Posting)
docid_n = 0

bigBook = {}


class Posting(object):

    def __init__(self, docid, tfidf, fields, pos):
        """
        Construct a new 'Posting' object.
        :param docid: Doc id, a int
        :param tfidf: Frequency count or TF-IDF
        :param fields: Fields, not in use yet
        :param pos: Positions, not in use yet
        :return: returns nothing
        """
        self.docid = docid
        self.tfidf = tfidf
        self.fields = fields
        self.pos = pos


def build_index(document):
    """
    Storing inverted_list as indexer.
    :param document: a json file.
    :return: returns nothing
    """

    global bigBook

    with open(document)as f:
        data = json.load(f)
        print(data["content"])

    soup = BeautifulSoup(data["content"], 'html.parser')

    s = soup.get_text()

    wordList = simple_tokenize(s.split())
    bigBook = combineFreq(wordList, bigBook)
    b_sorted = sorted(bigBook.items(), reverse=True,
                      key=operator.itemgetter(1))
    for token, freq in b_sorted:
        if token not in inverted_list.keys():
            print(token, freq)
            inverted_list[token] = list()
        inverted_list[token].append(Posting(docid_n, freq, 0, 0))

    f.close()


# def parse_json(data):
#     """
#     Parse json file into contents that can read by simple_tokenize
#     :param data: json file stored as dict
#     :return: list of words


if __name__ == '__main__':
    """
    For M1 testing purpose
    """
    print("Enter directory:")
    directory = input()
    for filename in os.listdir(directory):
        abs_file_path = directory + "/" + filename
        print(abs_file_path)
        if filename.endswith('.json'):
            docid_n += 1
            build_index(abs_file_path)
            print50(bigBook)

            # print(inverted_list)

            # print the keys, then the values (a list)
            for x in inverted_list:
                i = 0  # for checking if a comma needs to be printed
                print(x, ": [", end=" ")

                listOfPosting = inverted_list[x]
                for z in listOfPosting:  # print the value(the list of posting)
                    if i > 0:
                        print(",", end=" ")
                    print("(", z.docid, ",", z.tfidf, ")", end="")
                    i += 1  # this is only for checking if a comma should be added, nothing else

                print("]")
