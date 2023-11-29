import mysql.connector

db = mysql.connector.connect(
    HOST="localhost",
    USER="root",
    PASSWORD="162534",
    DB="escueladb"
)

cursor=db.cursor()