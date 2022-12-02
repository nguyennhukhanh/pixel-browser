import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1029384756"
)

cur = mydb.cursor()
cur.execute("CREATE DATABASE browserhistory")
