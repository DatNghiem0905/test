from flask import Flask, request
from pyvi import ViTokenizer
from gensim.models import KeyedVectors 
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
import traceback
import nltk
import sys
import pickle
import re 
import mysql.connector
from database import get_data
from tts import textToSpeech
app = Flask(__name__)

nltk.download('punkt')

@app.route("/summarize-text", methods=["POST"])
def summarize():
	conn = mysql.connector.connect(
		host="127.0.0.1",
		port=3306,
		user="root",
		password="",
		database="qltintuc")
	mycursor = conn.cursor()
	mycursor.execute("SELECT Noi FROM tinbai WHERE id = (SELECT MAX(id) FROM tinbai)")
	contents = mycursor.fetchall()
	conn.close()

	contents_parsed = []
	for content in contents[0:10]:
		content=(''.join(content))
		contents_parsed.append(content.lower().strip().replace("<p>","").replace("</p>",""))  
	# print(contents_parsed[0])
	    
	sentences = nltk.sent_tokenize(contents_parsed[0])
	# print(sentences)
	w2v = KeyedVectors.load_word2vec_format('wiki.vi.model.bin', binary=True)
	X = []
	for sentence in sentences:
		sentence_tokenized = ViTokenizer.tokenize(sentence)
		words = sentence_tokenized.split(" ")
		sentence_vec = np.zeros((400))
		for word in words:
			if word in w2v.wv.vocab:
				sentence_vec += w2v.wv[word]
		X.append(sentence_vec)

	n_clusters = 5
	kmeans = KMeans(n_clusters = n_clusters)
	kmeans = kmeans.fit(X)
	   
	avg = []
	for j in range(n_clusters):
		idx = np.where(kmeans.labels_ == j)[0]
		avg.append(np.mean(idx))
	closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
	ordering = sorted(range(n_clusters), key=lambda k: avg[k])

	summary = ' '.join([sentences[closest[idx]] for idx in ordering])
	updateSum(summary)

	return "Done"

def updateSum(Tomtat):
	conn = mysql.connector.connect(
		host="127.0.0.1",
		port=3306,
		user="root",
		password="",
		database="qltintuc")

	mycursor = conn.cursor()
	sql = """UPDATE tinbai SET TomTat = %s order by id desc limit 1 """
	mycursor.execute(sql, (Tomtat,))
	conn.commit()
	print(mycursor.rowcount, "record(s) affected")
	conn.close()

@app.route("/Link-tts", methods=["POST"])
def linktospeech():
    def updateData(idnhom , links):
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="qltintuc")

        mycursor = conn.cursor()
        sql = """UPDATE tinbai SET Link = %s WHERE id = %s """
        value = (links, idnhom)
        mycursor.execute(sql, value)
        conn.commit()
        print(mycursor.rowcount, "record(s) affected")
        print(links)
        conn.close()

    for item in get_data():
        idnhom = item[0]
        content = item[1]
    try:
        links = textToSpeech(content)
        updateData(idnhom , links)
    except:
        print(traceback.print_exc())

    return "Done"	  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)