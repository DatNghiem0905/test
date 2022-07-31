import mysql.connector

def insert_data(TieuDe, NoiDung, TomTat, idTheLoai):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="dat",
        password="dat",
        database="qltintuc")

    mycursor = conn.cursor()
    sql = """INSERT INTO tinbai (TieuDe , NoiDung, TomTat, idTheLoai ) VALUES (%s, %s, %s, %s, %s)"""
    value = (TieuDe, NoiDung, TomTat, idTheLoai)
    mycursor.execute(sql, value)
    conn.commit()
    print(mycursor.rowcount, "record inserted.")
    conn.close()

def get_data():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="qltintuc")

    mycursor = conn.cursor()
    mycursor.execute("SELECT id, TomTat FROM tinbai WHERE id = (SELECT MAX(id) FROM tinbai)")
    myresult = mycursor.fetchall()
    conn.close()
    return myresult

def summarize_data():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="qltintuc")

    mycursor = conn.cursor()
    mycursor.execute("SELECT id, NoiDung FROM tinbai WHERE id = (SELECT MAX(id) FROM tinbai)")
    myresult = mycursor.fetchall()
    conn.close()
    return myresult

def updateData(idnhom , links):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="qltintuc")

    mycursor = conn.cursor()
    sql = """UPDATE tinbai SET Link = %s WHERE id = %s"""
    value = (links, idnhom)
    mycursor.execute(sql, value)
    conn.commit()
    print(mycursor.rowcount, "record(s) affected")
    print(links)
    conn.close()

def updateSum(Tomtat):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="dat",
        password="dat",
        database="qltintuc")

    mycursor = conn.cursor()
    sql = """UPDATE tinbai SET TomTat = %s order by id desc limit 1 """
    mycursor.execute(sql, (Tomtat,))
    conn.commit()
    print(mycursor.rowcount, "record(s) affected")
    conn.close()   