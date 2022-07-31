# from urllib import response
from database import get_data
from tts import textToSpeech
import mysql.connector
import traceback
import requests

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
    print(idnhom)
    try:
        print(content)
        links = textToSpeech(content)
        updateData(idnhom , links)
    except:
        print(traceback.print_exc())
        

      
# def updateSum(Tomtat):
#     # print(Tomtat)
#     conn = mysql.connector.connect(
#         host="127.0.0.1",
#         port=3306,
#         user="root",
#         password="",
#         database="qltintuc")

#     mycursor = conn.cursor()
#     sql = """UPDATE tinbai SET TomTat = %s order by id desc limit 1  """
#     mycursor.execute(sql, (Tomtat,))
#     conn.commit()
#     print(mycursor.rowcount, "record(s) affected")
#     conn.close()
