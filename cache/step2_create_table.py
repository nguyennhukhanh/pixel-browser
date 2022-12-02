import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1029384756",
    database="browserhistory"
)

mycursor = mydb.cursor()

mycursor.execute(
    "CREATE TABLE cache (id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, address TEXT NOT NULL, timestamp varchar(255) NOT NULL)")
