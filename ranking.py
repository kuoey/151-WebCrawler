from bs4 import BeautifulSoup
import pickle
from retriever import *
from merger import *

def calc_tfidf():
    # assume index has been properly merged.
    totalfile = open('total', 'ab')
    N = 55393
    dbfile = open('index', 'rb')
    rankingfile = open('ranked_index', 'ab')
    pFile=open('subIndex', 'rb')
    dict={}
    d_counter=0
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            # [[123]],[[456]]
            print("-----------------------------")
            # dict = pickle.load(dbfile)
            subIndex = pickle.load(pFile)
            print(len(subIndex))
            for word in subIndex.keys():
                postings= search(word)
                print(len(dict.keys()))
                # print("word is :", word,len(dict[word]))
                if len(postings)>0:
                    counter=0
                    for posting in postings:
                        # print("Status",status)
                        # q_docid = status[0]
                        q_freq = posting[1]
                        tf = 1 + math.log(q_freq)
                        #TODO: test search()

                        idf = math.log(N / len(postings))
                        # idf=math.log(1942 / get_df(word))
                        tf_idf = tf * idf
                        tf_idf += posting[2]
                        postings[counter][3]=tf_idf
                        counter+=1
                dict[word]=postings
                d_counter+=len(postings)
                if d_counter==12000:

                    pickle.dump(dict,rankingfile)

                    dict.clear()
                    d_counter=0

        except(EOFError):
            break
    pickle.dump(dict, rankingfile)
    rankingfile.close()
if __name__ == '__main__':
    calc_tfidf()
