from database import get_data
from database import updateData
from tts import textToSpeech
import mysql.connector
import traceback
import requests
import numpy as np
from flask import Flask, request

app = Flask(__name__)

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