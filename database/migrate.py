import mysql.connector 

conn = mysql.connector.connect(
    host ="localhost",
    port = "3306",
    user = "victor",
    password = "alchemy97",
    database = "laravel_data" 
)
cursor = conn.cursor()


with open("laravel_data.sql") as f:
    sql = f.read()

cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()