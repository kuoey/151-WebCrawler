#     inverted_list = merger.get_results(q)
#     # print("Inverted_list",inverted_list)
#
#     if inverted_list!=[]:
#         temp=list()
#         for status in inverted_list:
#             # print("Status",status)
#             q_docid= status[0]
#             q_freq= status[1]
#             # if q!=queries[0]:
#             #     if q_docid in check_docid:
#             #         temp.append(q_docid)
#             #         tf = q_freq / get_wordcount(q_docid)
#             #         idf = math.log(N / len(inverted_list))
#             #         tf_idf = tf * idf
#             #         # print("TF_IDF", tf_idf)
#             #         if q_docid not in ranking.keys():
#             #             ranking[q_docid] = tf_idf
#             #         else:
#             #             ranking[q_docid] += tf_idf
#             #     else:
#             #         pass
#             # else:
#             check_docid.append(q_docid)
#             tf = q_freq / get_wordcount(q_docid)
#             idf = math.log(N / len(inverted_list))
#             tf_idf= tf * idf
#             tf_idf+=status[2]
#             # print("TF_IDF",tf_idf)
#             if q_docid not in ranking.keys():
#                 ranking[q_docid]=tf_idf
#             else:
#                 ranking[q_docid]+=tf_idf

# if len(temp)<len(check_docid):
#     check_docid=temp
# print("Check", check_docid)

# print("Rank:",rank)
# print(queries)
# openDBfile = open("index", 'rb')
# db = pickle.load(openDBfile)
# openURLfile = open("urls", 'rb')
# url = pickle.load(openURLfile)
# openWfile = open("words", 'rb')
# total_words = pickle.load(openWfile)
# db holds the inverted list that was put into dbfile
# openURLfile.close()
    # openDBfile.close()
    # openWfile.close()
"""
if not os.path.exists("index"):    # Checks for index file
    print("Error, couldn't find file: index")
    exit(0)

dbfile = open('index', 'rb')

dict = pickle.load(dbfile)

print(dict["learn"])
dbfile.close()
"""