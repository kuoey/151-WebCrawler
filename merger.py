import os
import pickle
from PartA import *


def get_results(word):
    dbfile = open('index', 'rb')
    results = []
    while 1:    # Horrible condition, never do this ever ever ever
        try:
            #[[123]],[[456]]
            dict = pickle.load(dbfile)
            if word in dict.keys():
                #results = results + dict[word]
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
    # subIndex = sorted(subIndex.items(), key=operator.itemgetter(0))

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


def search():
    fileREAD = open("SuperIndex.txt", "r")
    pFile = open('subIndex', 'rb')
    subIndex = pickle.load(pFile)
    pFile.close()
    myList = []
    word = input("Enter your search: ")
    if subIndex.get(word) is not None:
        for pair in subIndex[word]:
            fileREAD.seek(pair[0])
            strToList(myList, fileREAD.read(pair[1]))
    fileREAD.close()
    return myList


def strToList(pList, pString):
    n1 = -1
    n2 = -1
    postings = pString.split()
    for num in postings:
        num = re.sub(r'[^0-9]', '', num)
        if n1 == -1:
            n1 = int(num)
        else:
            n2 = int(num)
            pList.append((n1, n2))
            n1 = -1
            n2 = -1


if __name__ == '__main__':

    if not os.path.exists("index"):    # Checks for index file
        print("Error, couldn't find file: index")
        exit(0)

    myList = search()
    print(myList)

    # txt_merge()

    # pickle_merge()

    """
    dbfile = open('index', 'rb')

    dict = pickle.load(dbfile)

    print(dict["learn"])
    dbfile.close()
    """

    """
    if not os.path.exists("testIndex"):  # Checks for index file
        book1 = {}
        book2 = {}

        list1 = ['@#%^$', 'Word', 'Words!', '沼', 'te沼st', '1991اف_جي2']
        list2 = ['wOrD', 'JeReMy', '121*@#', 'pu#$ll', '#3PuSh', 'test', 'testing']

        list1 = simple_tokenize(list1)
        # The list is then fed to the dictionary bigBook using the combineFreq function
        book1 = combineFreq(list1, book1)

        # Same thing is done with second list
        list2 = simple_tokenize(list2)
        book2 = combineFreq(list2, book2)

        dSorted1 = sorted(book1.items(), key=operator.itemgetter(0))
        dSorted2 = sorted(book2.items(), key=operator.itemgetter(0))

        dbfile = open('testIndex', 'ab')
        pickle.dump(dSorted1, dbfile)
        pickle.dump(dSorted2, dbfile)
        dbfile.close()
    """

    #dbfile = open('index', 'rb')

    #test_dict = pickle.load(dbfile)
    #print(test_dict)

    #test_dict = pickle.load(dbfile)

    #print(test_dict)

    # print(get_results("2"))

    #dbfile.close()

    # Test merging dictionaries together
    """
    mBook = {}
    sBook = {}



    mBook["mentor"] = [(1,8),(2,8),(3,8)]
    sBook["mentor"] = [(293,2),(479,2),(559,2),(563,2),(1032,2),(1053,2)]
    sBook["dab"] = [(69,420)]

    for entry in sBook:
        if entry in mBook:
            mBook[entry] = mBook[entry] + sBook[entry]
        else:
            mBook[entry] = sBook[entry]

    print(mBook)
    """
