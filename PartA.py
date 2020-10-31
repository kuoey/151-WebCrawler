# Part A

import re  # Regex
import sys  # Gets commands line args
import os  # Testing file paths
import operator  # Used for sorting dictionaries

commonList = ["a", "about", "above", "after", "again", "against",
              "all", "am", "an", "and", "any", "are",
              "arent", "as", "at", "be", "because", "been",
              "before", "being", "below", "between", "both", "but",
              "by", "cant", "cannot", "could", "couldnt", "did",
              "didnt", "do", "does", "doesnt", "doing", "dont",
              "down", "during", "each", "few", "for", "from",
              "further", "had", "hadnt", "has", "hasnt", "have",
              "havent", "having", "he", "hed", "hell", "hes",
              "her", "here", "heres", "hers", "herself", "him",
              "himself", "his", "how", "hows", "i", "id",
              "ill", "im", "ive", "if", "in", "into",
              "is", "isnt", "it", "its", "its", "itself",
              "lets", "me", "more", "most", "mustnt", "my",
              "myself", "no", "nor", "not", "of", "off",
              "on", "once", "only", "or", "other", "ought",
              "our", "ours	ourselves", "out", "over", "own", "same",
              "shant", "she", "shed", "shell", "shes", "should",
              "shouldnt", "so", "some", "such", "than", "that",
              "thats", "the", "their", "theirs", "them", "themselves",
              "then", "there", "theres", "these", "they", "theyd",
              "theyll", "theyre", "theyve", "this", "those", "through",
              "to", "too", "under", "until", "up", "very",
              "was", "wasnt", "we", "wed", "well", "were",
              "weve", "werent", "what", "whats", "when",
              "whens", "where", "wheres", "which", "while", "who",
              "whos", "whom", "why", "whys", "with", "wont",
              "would", "wouldnt", "you", "youd", "youll", "youre",
              "youve", "your", "yours", "yourself", "yourselves"]

""" tokenize N TIME COMPLEXITY: O(n)
This method reads through each word once and puts them in a list without
repeating.
"""


def tokenize(filepath):
    tokens = []
    if os.path.exists(filepath):  # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
        with open(filepath, 'r', encoding="utf-8") as f:
            try:  # Catches files that can't be read
                for line in f:
                    for word in line.split():
                        try:  # Catches words that can't be tokenized
                            res = re.sub(r'[^A-Za-z0-9]', '', word)  # Use regex to remove non alpha numerics
                            res = res.lower()
                            if res != '' and res not in commonList:  # Does not allow blank tokens
                                tokens.append(res)
                        except:  # Skips bad words
                            pass
                f.close()
            except:
                print('Error: File could not be read. Please use a readable text file as input.')
                sys.exit()

    else:
        print('Error: File not found, please check your file parameters.')
        sys.exit()
    return tokens


"""computeWordFrequencies N TIME COMPLEXITY: O(n)
This method reads through the list and logs the results in a dictionary.
It takes n time to read through the list and takes constant time to
record the results since accessing a dictionary/adding to 
it is like a hash lookup.
"""


def computeWordFrequencies(tokenList):
    myBook = {}
    for word in tokenList:
        if word in myBook:
            myBook[word] = myBook[word] + 1
        else:
            myBook[word] = 1
    return myBook


""" print N TIME COMPLEXITY: O(n log n)
This method takes the contents of a dictionary and sorts them into a list of tuples
by python's default sorting method. Sorting takes n log n time.
"""


def aPrint(freqMap):
    dSorted = sorted(freqMap.items(), reverse=True,
                     key=operator.itemgetter(1))  # https://docs.python.org/2/howto/sorting.html
    for entry in dSorted:
        print('{} => {}'.format(entry[0], entry[1]))


# Extra functions for assignment 2
# Takes a list strings and turns them into proper tokens
def simple_tokenize(tokens):
    counter = 0
    while counter < len(tokens):
        res = re.sub(r'[^A-Za-z0-9]', '', tokens[counter])  # Use regex to remove non alpha numerics
        res = res.lower()
        #print("res: {}".format(res))
        if res == '' or res in commonList:  # Does not allow blank tokens or common words
            tokens.pop(counter)
        else:
            tokens[counter] = res
            counter += 1
    return tokens


# Takes a dictionary and list of words and adds to the dictionary
def combineFreq(tokenList, myBook):
    for word in tokenList:
        if word in myBook:
            myBook[word] = myBook[word] + 1
        else:
            myBook[word] = 1
    return myBook


# Prints the top 50 common words from a dictionary
def print50(freqMap):
    dSorted = sorted(freqMap.items(), reverse=True,
                     key=operator.itemgetter(1))  # https://docs.python.org/2/howto/sorting.html
    counter = 1
    for entry in dSorted:
        print("{}: {} => {}".format(counter, entry[0], entry[1]))  # Code to test number of entries
        
		# print(entry[0])
        if counter == 50:
            break
        counter += 1


# Demo for combining multiple lists of words into 1 dictionary
if __name__ == "__main__":
    bigBook = {}     # Initially empty dictionary, it will store the count of all words processed

    list1 = ['@#%^$', 'Word', 'Words!', '沼', 'te沼st', '1991اف_جي2']
    list2 = ['wOrD', 'JeReMy', '121*@#', 'pu#$ll', '#3PuSh', 'test', 'testing']

    # The first list goes through simple_tokenize function to get correct tokens
    list1 = simple_tokenize(list1)
    # The list is then fed to the dictionary bigBook using the combineFreq function
    bigBook = combineFreq(list1, bigBook)

    # Same thing is done with second list
    list2 = simple_tokenize(list2)
    bigBook = combineFreq(list2, bigBook)

    # After all the lists are combined, we can print the top 50 using print50
    print50(bigBook)
