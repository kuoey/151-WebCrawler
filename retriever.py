import re
import os
import requests
import json
from PartA import *
from tkinter import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pickle
import math
import webbrowser
import merger

ranking = dict()
check_docid = []
# added by eric
urlArray = []
labels = []  # creates an empty list for your labels


# added by eric


def retrieve(query):
    global check_docid
    global urlArray
    query = str(query)

    queries = simple_tokenize(query.split())
    # print(queries)
    # openDBfile = open("index", 'rb')
    # db = pickle.load(openDBfile)
    # openURLfile = open("urls", 'rb')
    # url = pickle.load(openURLfile)
    # openWfile = open("words", 'rb')
    # total_words = pickle.load(openWfile)
    # db holds the inverted list that was put into dbfile
    N = 55393

    for q in queries:
        inverted_list = merger.get_results(q)
        # print("Inverted_list",inverted_list)

        if inverted_list:
            temp = list()
            for status in inverted_list:
                # print("Status",status)
                q_docid = status[0]
                q_freq = status[1]
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
                tf_idf = tf * idf
                # print("TF_IDF",tf_idf)
                if q_docid not in ranking.keys():
                    ranking[q_docid] = tf_idf
                else:
                    ranking[q_docid] += tf_idf

                # if len(temp)<len(check_docid):
                #     check_docid=temp
        # print("Check", check_docid)
    counter = 0
    rank = {}
    # print(ranking)
    for i in check_docid:
        if i not in rank:
            rank[i] = ranking[i]
    ranking.clear()
    # print("Rank:",rank)
    urlArray = []
    for k, v in sorted(rank.items(), key=lambda item: item[1], reverse=True):
        # should add to array of strings, then have the GUI app read from that array
        urlArray.append(get_urls(k))  # for now, append then print
        # print(get_urls(k))
        counter += 1
        if counter == 5:
            break
    # openURLfile.close()
    # openDBfile.close()
    # openWfile.close()


def get_urls(word):
    dbfile = open('urls', 'rb')
    results = ""
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            # [[123]],[[456]]
            dict = pickle.load(dbfile)
            if word in dict.keys():
                results = dict[word]
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
                results = dict[word]
        except(EOFError):
            break
    dbfile.close()
    return results


# added by eric
# creates application for GUI
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.fram = Frame(self.master)
        Label(self.fram, text='Google2').pack(side=LEFT)
        # adding of single line text box
        self.edit = Entry(self.fram)

        # positioning of entry text box
        self.edit.pack(side=LEFT, fill=BOTH, expand=1)

        # setting focus
        self.edit.focus_set()

        # adding of search button
        self.butt = Button(self.fram, text='Search')
        self.butt["command"] = self.find
        # binds return key to the find function so the user can press search or return key
        self.master.bind('<Return>', self.find)
        self.butt.pack(side=RIGHT)

        self.fram.pack(side=TOP)

        # creates label "search results" and places it on left side
        self.labelSearch = Label(root, text="Search Results:", anchor='w')  # set your text
        self.labelSearch.pack(fill='both')

    # it displays the search results
    # the event =0 is needed for the return key, pls dont delete
    def find(self, event=0):
        # first destroy any hyperlinks if there are any (from previous search)
        for label in labels:
            label.destroy()

        # returns to widget currently in focus
        s = self.edit.get()
        # s is the word that the user typed into the search box
        if s:  # if the user has typed in a word in the search box:
            term = s.lower()
            retrieve(term)

            # go through the array of top 5 urls and create labels that are hyperlinks
            for i in urlArray:
                print("temp ", i)

                self.label = Label(root, text=i + '\n', fg="blue", cursor="hand2", anchor='w')  # set your text
                self.label.pack(fill='both')
                self.label.bind("<Button-1>", lambda event, url=i: webbrowser.open(url))
                labels.append(self.label)  # appends the label to the list for further use

        self.edit.focus_set()


# added by eric

if __name__ == '__main__':
    # the GUI stuff will be started here
    # print("Please enter the term:")
    # term = input().lower()
    # retrieve(term)

    # added by eric
    root = Tk()
    root.geometry("1024x576")
    app = Application(master=root)
    app.mainloop()
    # added by eric
