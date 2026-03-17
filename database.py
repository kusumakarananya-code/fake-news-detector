import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ananya@19",
    database="fake_news_project"
)

cursor = connection.cursor()

print("Database Connected Successfully")

