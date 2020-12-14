import re
import os
import requests
import json
import pickle
import math
import webbrowser
from PartA import *
from tkinter import *
from tkinter import messagebox
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from merger import *

ranking = dict()
check_docid = []
N = 55393
# added by eric
urlArray = []
labels = []  # creates an empty list for your labels


# todo Lydia will explain
def retriever_test(query, fileREAD, subIndex):
    global check_docid
    global urlArray
    docids = set()
    # check_docid=[]
    ranking = dict()
    # result=dict()
    # idf = []
    # fileREAD = open("SuperIndex.txt", "r")
    # pFile = open('subIndex', 'rb')
    # subIndex = pickle.load(pFile)
    # pFile.close()
    # query = str(input("Enter your search: "))
    start_time = datetime.datetime.now()
    queries = simple_tokenize(list(set(query.split())))  # part A stuffs

    for q in queries:
        postings = simple_search(q, fileREAD, subIndex)
        if len(postings) > 0:
            # idf.append(math.log(N / len(postings)))
            if len(docids) == 0:
                docids = set(i[0] for i in postings)
            else:
                docids &= set(i[0] for i in postings)
            # print("Posting",postings)
            for i in postings:
                if i[0] in docids:
                    if i[0] in ranking.keys():
                        # if i[0] not in check_docid:
                        # print(ranking[i[0]],((1 + math.log(i[1])),i[2]))
                        ranking[i[0]] += (float(i[1]) + i[2] * 5 * (math.log(N / len(postings))))
                    else:
                        ranking[i[0]] = float(i[1]) + i[2] * 5 * (math.log(N / len(postings)))
                    # check_docid.append(i[0])
        else:
            print("Nothing found")
    counter = 0
    urlArray.clear()
    for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True):
        urlArray.append(get_urls(k))
        counter += 1
        if counter == 5:
            break
    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    execution_time = time_diff.total_seconds() * 1000
    print(execution_time, "ms")


def get_urls(word):
    dbfile = open('urls', 'rb')
    results = ""
    while 1:  # Horrible condition, never do this ever ever ever ever
        try:
            dict = pickle.load(dbfile)
            if word in dict.keys():
                results = dict[word]
                break
        except(EOFError):
            break
    dbfile.close()
    return results


def get_wordcount(word):
    dbfile = open('words', 'rb')
    results = ""
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            dict = pickle.load(dbfile)
            if word in dict.keys():
                results = dict[word]
        except(EOFError):
            break
    dbfile.close()
    return results


# TODO EXPLAIN ERIC
# added by eric
# creates application for GUI
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()
        self.create_widgets()

        pFile = open('subIndex', 'rb')
        self.subIndex = pickle.load(pFile)
        pFile.close()
        self.file = open("SuperIndex.txt", "r")

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
        labelsEmpty = len(labels) == 0

        # returns to widget currently in focus
        s = self.edit.get()
        # s is the word that the user typed into the search box
        if s:  # if the user has typed in a word in the search box:
            term = s.lower()
            retriever_test(term, self.file, self.subIndex)

            # go through the array of top 5 urls and create labels that are hyperlinks
            labelIndex = 0
            for i in urlArray:
                if labelsEmpty:
                    print("temp ", i)

                    self.label = Label(root, text=i + '\n', fg="blue", cursor="hand2", anchor='w')  # set your text
                    self.label.pack(fill='both')
                    self.label.bind("<Button-1>", lambda event, url=i: webbrowser.open(url))
                    labels.append(self.label)  # appends the label to the list for further use
                else:
                    print("temp ", i)
                    labels[labelIndex].config(text=i + '\n')
                    labels[labelIndex].bind("<Button-1>", lambda event, url=i: webbrowser.open(url))
                    labelIndex += 1

        self.edit.focus_set()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.file.close()
            root.destroy()


# added by eric

# used GUI called Tkinter
if __name__ == '__main__':
    root = Tk()
    root.geometry("1024x576")

    app = Application(master=root)
    app.master.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
