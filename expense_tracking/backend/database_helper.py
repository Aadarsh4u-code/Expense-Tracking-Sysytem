import mysql.connector

connection = mysql.connector.connect(
    host = "localhost",
    user= "root",
    port = "3306",
    password = "@Mysql12345",
    database = "expense_manager",
)
if connection.is_connected:
    print("Connections successful...")
else:
    print("Connection Faild to connect a database.")
