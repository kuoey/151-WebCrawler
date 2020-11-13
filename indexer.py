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
dump_counter=0
bigBook = {}
token_num= set()


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
    global dump_counter
    global docid_n
    docid_n += 1
    dump_counter += 1
    with open(document)as f:
        data = json.load(f)
        # print(data["content"])

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
        inverted_list[token].append(Posting(docid_n, freq, 0, 0))

    if dump_counter== 500:
        dbfile = open(str(docid_n), 'ab')
        pickle.dump(inverted_list, dbfile)
        dump_counter=0
        inverted_list.clear()
        dbfile.close()
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
    if os.path.exists("output.txt"):    # Resets the output file
        os.remove("output.txt")

    fileOUT = open("output.txt", "a")

    print("Enter directory:")
    directory = input()
    for folder in os.listdir(directory):    # Runs through each folder
        abs_file_path = directory + "/" + folder    # Path to each folder within DEV folder
        print(abs_file_path)
        for file in os.listdir(abs_file_path):  # Runs through each file in a folder
            print(file)
            final_path = abs_file_path + "/" + file     # Path to json files in folders
            print(final_path)
            if file.endswith('.json'):

                build_index(final_path)
                # print50(bigBook)

    if len(inverted_list)!=0:
        dbfile = open(str(docid_n), 'ab')
        pickle.dump(inverted_list, dbfile)
        inverted_list.clear()
        dbfile.close()
    print(len(token_num))
    # print(inverted_list)


    # print the keys, then the values (a list)
    for x in inverted_list:
        i = 0  # for checking if a comma needs to be printed
        print(x, ": [", end="")
        fileOUT.write("{} [".format(x))

        listOfPosting = inverted_list[x]
        for z in listOfPosting:  # print the value(the list of posting)
            if i > 0:
                print(",", end=" ")
                fileOUT.write(",")
            print("(", z.docid, ",", z.tfidf, ")", end="")
            fileOUT.write("({},{})".format(str(z.docid), str(z.tfidf)))
            i += 1  # this is only for checking if a comma should be added, nothing else

        print("]")
        fileOUT.write("]\n")
    fileOUT.close()
