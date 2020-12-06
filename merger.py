import datetime
import os
import pickle
from PartA import *


def get_results(word):
    dbfile = open('index', 'rb')
    results = []
    while 1:    # Horrible condition, never do this ever ever ever
        try:
            dict = pickle.load(dbfile)
            if word in dict.keys():
                for entry in dict[word]:
                    results.append(entry)


        except(EOFError):
            break
    dbfile.close()
    return results


def pickle_merge():
    oldfile = open('index', 'rb')
    fullBook = {}
    while 1:    # Horrible condition, never do this ever ever ever
        try:
            if len(fullBook) == 0:
                fullBook = pickle.load(oldfile)
            else:
                sDict = pickle.load(oldfile)
                for entry in sDict:
                    if entry in fullBook:
                        fullBook[entry] = fullBook[entry] + sDict[entry]
                    else:
                        fullBook[entry] = sDict[entry]
                    sDict[entry] = "done"        # Attempt to save on memory
                sDict.clear()
            print("dict saved")

        except EOFError:
            break
    oldfile.close()

    if os.path.exists("superIndex"):  # Refresh superIndex
        os.remove("superIndex")

    newfile = open('superIndex', 'wb')
    pickle.dump(fullBook, newfile)
    newfile.close()


def make_sub_index():
    oldfile = open('index', 'rb')
    subIndex = dict()
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            sDict = pickle.load(oldfile)
            for entry in sDict:
                subIndex[entry] = (-1, 0)

        except(EOFError):
            break
    oldfile.close()
    return subIndex


def slow_txt_merge():
    print("Creating sub index")
    subIndex = make_sub_index()                 # Make index of indexes
    for entry in subIndex:                      # For each word,
        print("Saving " + entry + " to txt...")
        results = get_results(entry)            # get the results from the dicts
        fileOUT = open("SuperIndex.txt", "a")   # and write the word and the entries into a txt
        fileOUT.write(entry + " ")              # Save the pointer position and number of chars
        pointer = fileOUT.tell()                # That make up the word's results
        fileOUT.write(str(results))
        adv = fileOUT.tell() - pointer
        fileOUT.close()
        subIndex[entry] = (pointer, adv)        # Save pointer and adv as a pair to use for reading

    print("Saving sub index...")
    newfile = open('subIndex', 'wb')            # Save the sub index to pickle so it can be retrieved again
    pickle.dump(subIndex, newfile)
    newfile.close()
    subIndex.clear()
    print("Done")


def txt_merge():
    pFile = open('index', 'rb')
    fileOUT = open("SuperIndex.txt", "a")
    subIndex = {}
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            pDict = pickle.load(pFile)
            print("Dictionary Loaded")
            for word in pDict.keys():
                # results = results + dict[word]
                fileOUT.write(word + " ")
                pointer = fileOUT.tell()
                fileOUT.write(str(pDict[word]))
                adv = fileOUT.tell() - pointer
                if subIndex.get(word) is None:
                    subIndex[word] = []
                subIndex[word].append((pointer, adv))
            print("Saved")
        except EOFError:
            break
    pFile.close()
    fileOUT.close()

    newfile = open('subIndex', 'wb')  # Save the sub index to pickle so it can be retrieved again
    pickle.dump(subIndex, newfile)
    newfile.close()
    subIndex.clear()


def search(word):
    fileREAD = open("SuperIndex.txt", "r")
    pFile = open('subIndex', 'rb')
    subIndex = pickle.load(pFile)
    pFile.close()
    myList = []
    # word = input("Enter your search: ")
    if subIndex.get(word) is not None:
        for pair in subIndex[word]:
            fileREAD.seek(pair[0])
            strToList(myList, fileREAD.read(pair[1]))
    fileREAD.close()
    return myList


def simple_search(word, fileREAD, subIndex):    # Word being searched, open file pointer to superindex, and a subindex that is equal to the first load of pickle file
    aList = []
    if subIndex.get(word) is not None:
        for pair in subIndex[word]:
            fileREAD.seek(pair[0])
            strToList(aList, fileREAD.read(pair[1]))
    return aList


def strToList(pList, pString):
    n1 = -1
    n2 = -1
    n3 = -1
    postings = pString.split()
    for num in postings:
        num = re.sub(r'[^0-9]', '', num)
        if n1 == -1:
            n1 = int(num)
        elif n2 == -1:
            n2 = int(num)
        elif n3 == -1:
            n3 = int(num)
        else:
            pList.append([n1, n2, n3, int(num)])
            n1 = -1
            n2 = -1
            n3 = -1


if __name__ == '__main__':

    if not os.path.exists("index"):    # Checks for index file
        print("Error, couldn't find index, please run indexer.py first.")
        exit(0)

    txt_merge()
    os.remove("index")

