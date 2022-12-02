import mysql.connector
from datetime import datetime
from final_variable import host, user, password, database

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()


def save_history(arg):
    dt = datetime.now()

    sql = "INSERT INTO cache (address, timestamp) VALUE (%s, %s)"
    val = (arg, dt)
    mycursor.execute(sql, val)

    mydb.commit()

    print("Đã lưu vào lịch sử duyệt Web", arg)
