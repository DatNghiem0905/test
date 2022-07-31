from database import summarize_data
from database import updateSum
import mysql.connector
import traceback
import numpy as np
from pyvi import ViTokenizer
import nltk
from gensim.models import KeyedVectors 
from gensim.models import Word2Vec
import sys
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import pickle
import re 


conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="qltintuc")

mycursor = conn.cursor()
mycursor.execute("SELECT Noi FROM tinbai WHERE id = (SELECT MAX(id) FROM tinbai)")
myresult = mycursor.fetchall()
conn.close()


def updateSum(Tomtat):
    # print(Tomtat)
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="qltintuc")

    mycursor = conn.cursor()
    sql = """UPDATE tinbai SET TomTat = %s order by id desc limit 1  """
    mycursor.execute(sql, (Tomtat,))
    conn.commit()
    print(mycursor.rowcount, "record(s) affected")
    conn.close()

contents=myresult

contents_parsed = []
for content in contents[0:10]:
    content=(''.join(content))
    contents_parsed.append(content.lower().strip().replace("<p>","").replace("</p>",""))  
print(contents_parsed[0])
    
nltk.download('punkt')
sentences = nltk.sent_tokenize(contents_parsed[0])
print(sentences)
model= '/wiki.vi.model.bin'
w2v= KeyedVectors.load_word2vec_format(model, binary=True)
vocab = w2v.wv.vocab

# X = []
#print(w2v.wv["hi"].shape)
#print(np.zeros(400).shape)
# for sentence in sentences:
#     sentence = ViTokenizer.tokenize(sentence)
#     words = sentence.split(" ")
#     sentence_vec = np.zeros(400)
#     for word in words:
#         if word in vocab:
#             np.sumsentence_vec.sum()
#             sentence_vec.append(w2v.wv[word])
#     print(np.array(sentence_vec).shape)
#     for i in range(100-len(sentence_vec)):
#       sentence_vec.append(np.zeros(400))
#     print(np.array(sentence_vec).shape)
#     X.append(sentence_vec)
# print(np.array(X).shape)

X = []
for sentence in sentences:
    sentence_tokenized = ViTokenizer.tokenize(sentence)
    words = sentence_tokenized.split(" ")
    sentence_vec = np.zeros((400))
    for word in words:
        if word in vocab:
            sentence_vec+=w2v.wv[word]
    X.append(sentence_vec)

n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters)
kmeans = kmeans.fit(X)
   
avg = []
for j in range(n_clusters):
    idx = np.where(kmeans.labels_ == j)[0]
    avg.append(np.mean(idx))
closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
ordering = sorted(range(n_clusters), key=lambda k: avg[k])

summary = ' '.join([sentences[closest[idx]] for idx in ordering])

# summ=list(summary)
#for item in summarize_data():
	##try:
	    #data = summary
        #updateSum(idnhom , data)
	#except:
		#print(traceback.print_exc())  

updateSum(summary)