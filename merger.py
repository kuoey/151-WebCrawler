import os
import pickle
from PartA import *


def get_results(word):
    dbfile = open('index', 'rb')
    results = []
    while 1:    # Horrible condition, never do this ever ever ever
        try:
            dict = pickle.load(dbfile)
            for entry in dict[word]:
                results.append(entry)
        except(EOFError):
            break
    dbfile.close()
    return results


if __name__ == '__main__':
    """
    if not os.path.exists("index"):    # Checks for index file
        print("Error, couldn't find file: index")
        exit(0)

    dbfile = open('index', 'rb')

    dict = pickle.load(dbfile)

    print(dict["learn"])
    dbfile.close()
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

    dbfile = open('index', 'rb')

    test_dict = pickle.load(dbfile)
    print(test_dict)

    test_dict = pickle.load(dbfile)
    print(test_dict)

    print(get_results("2"))

    dbfile.close()








