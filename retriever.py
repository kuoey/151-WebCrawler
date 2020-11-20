ranking=dict()

def retrieve(query):
    query = str(query)
    queries = query.split()
    openDBfile = open("index", 'rb')
    db = pickle.load(openDBfile)
    openURLfile = open("urls", 'rb')
    url = pickle.load(openURLfile)
    # db holds the inverted list that was put into dbfile
    for q in queries:
        if q in db.keys():
            for status in db[q]:
                q_docid= status[0]
                q_freq= status[1]

                tf = q_freq / total_worlds[q_docid]
                idf = math.log(N / len(db[query]))
                tf_idf= tf * idf
                if q_docid not in ranking.keys():
                    ranking[q_docid]=tf_idf
                else:
                    ranking[q_docid]+=tf_idf
        print(keys, '=>', db[keys])
    counter=0
    while(counter<=5):
        for k, v in sorted(x.items(), key=lambda item: item[1]):
            print(url[k])
            counter+=1
    openURLfile.close()
    openDBfile.close()