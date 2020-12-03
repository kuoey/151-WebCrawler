from bs4 import BeautifulSoup


def calc_tfidf():
    # assume index has been properly merged.
    dbfile = open('index', 'rb')
    rankingfile=open('ranked_index','ab')
    while 1:  # Horrible condition, never do this ever ever ever
        try:
            # [[123]],[[456]]
            dict = pickle.load(dbfile)
            for word in dict.keys():
                if dict[word]!=[]:
                    counter=0
                    for status in dict[word]:
                        # print("Status",status)
                        q_docid = status[0]
                        q_freq = status[1]
                        tf = q_freq / get_wordcount(q_docid)
                        #TODO: test search()
                        idf = math.log(N / len(search(word)))
                        tf_idf = tf * idf
                        tf_idf += status[2]
                        dict[word][counter][3]=tf_idf
                        counter+=1
            pickle.dump(dict,rankingfile)

        except(EOFError):
            break
    rankingfile.close()
