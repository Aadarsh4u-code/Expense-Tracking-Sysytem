import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "localhost",
        user= "root",
        port = "3306",
        password = "@Mysql12345",
        database = "expense_manager",
    )
    if connection.is_connected:
        print("Connections established...")
    else:
        print("Connection Faild to connect a database.")
    
    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_record():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()
        return data

def fetch_expenses_for_date(expenses_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date= %s",(expenses_date,))
        data = cursor.fetchall()
        return data

def fetch_expenses_for_date_between(expenses_from_date, expenses_to_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date BETWEEN %s AND %s ORDER BY expense_date",(expenses_from_date, expenses_to_date))
        data = cursor.fetchall()
        return data

def insert_expenses(expense_date, amount, category, notes):
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)", (expense_date, amount, category, notes))

        # Verify if data is inserted and print success message
        if cursor.rowcount > 0:  # rowcount tells how many rows were affected
            print("Success! Data inserted into the database.")
        else:
            print("Error: Data not inserted.")

def delete_expenses_item(id):
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))

        # Verify if data is inserted and print success message
        if cursor.rowcount > 0:  # rowcount tells how many rows were affected
            print("Success! Data deleted from database.")
        else:
            print("Error: Data not deleted.")

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

        # Verify if data is inserted and print success message
        if cursor.rowcount > 0:  # rowcount tells how many rows were affected
            print("Success! Data deleted from database.")
        else:
            print("Error: Data not deleted.")

def get_expense_summary(expenses_from_date, expenses_to_date):
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT category, SUM(amount) as total 
                        FROM expenses WHERE expense_date 
                        BETWEEN %s AND %s
                        GROUP BY category;""", 
                        (expenses_from_date, expenses_to_date)
                    )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    # fetch_all_record()
    fetch_expenses_for_date("2024-08-05")
    # fetch_expenses_for_date_between("2024-08-05", "2024-09-05")
    # insert_expenses("2025-03-10", 20, "Grocery", "ALDI")
    # delete_expenses_item("40")
    # get_expense_summary("2024-08-05", "2024-09-05")