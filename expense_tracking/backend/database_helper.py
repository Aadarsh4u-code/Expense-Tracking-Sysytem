import mysql.connector
from contextlib import contextmanager
from expense_tracking.logger import logging
import sys

# Get the file name
# logger = logging.getLogger('database_helper')
logger = logging.getLogger('database_helper')

# Create connection with Database.
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

# Get all expense data.
def fetch_all_record():
    logging.info(f"{fetch_all_record.__name__} called to fetch all expenses data.")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()
        return data

# Get all expense data for selected date.
def fetch_expenses_for_date(expenses_date):
    logging.info(f"{fetch_expenses_for_date.__name__} called to fetch expenses with date {expenses_date}.")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date= %s",(expenses_date,))
        data = cursor.fetchall()
        return data

# Get expense data for selected id.
def fetch_expenses_for_id(expenses_id):
    logging.info(f"{fetch_expenses_for_id.__name__} called to fetch expenses with date {expenses_id}.")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE id= %s",(expenses_id,))
        data = cursor.fetchall()
        return data
    
# Update expense data for selected id.
def update_expenses_for_id(expenses_id, expense_date, amount, category, notes):
    logging.info(f"{update_expenses_for_id.__name__} called to update expenses with id {expenses_id}.")
    query = """ 
                INSERT INTO expenses (id, expense_date, amount, category, notes) VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                expense_date = VALUES(expense_date),
                amount = VALUES(amount),
                category = VALUES(category),
                notes = VALUES(notes);
            """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, (expenses_id, expense_date, amount, category, notes))
        if cursor.rowcount > 0:
            logging.info("Success! Data updated in the database.")
        else:
            logging.error("Error: Data not updated.")

# Get expense data for given date range.
def fetch_expenses_for_date_between(expenses_from_date, expenses_to_date):
    logging.info(f"{fetch_expenses_for_date_between.__name__} called to fetch expenses from {expenses_from_date} to {expenses_to_date} date.")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date BETWEEN %s AND %s ORDER BY expense_date DESC",(expenses_from_date, expenses_to_date))
        data = cursor.fetchall()
        return data

# Insert expense data for given date.
def insert_expenses(expense_date, amount, category, notes):
    logging.info(f"{insert_expenses.__name__} called to store expenses with expense date: {expense_date}, amount: {amount}, category: {category} and notes: {notes}.")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)", (expense_date, amount, category, notes))

        # Verify if data is inserted and print success message
        if cursor.rowcount > 0:  # rowcount tells how many rows were affected
            print("Success! Data inserted into the database.")
        else:
            print("Error: Data not inserted.")

# Delete expense data for given id.
def delete_expenses_item(ids):
    logging.info(f"{delete_expenses_item.__name__} called to delete expense with id: {ids}.")
    for id in ids:
        with get_db_cursor(commit = True) as cursor:
            cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))

            # Verify if data is inserted and print success message
            if cursor.rowcount > 0:  # rowcount tells how many rows were affected
                print("Success! Data deleted from database.")
            else:
                print("Error: Data not deleted.")

# Delete expense data for given date.
def delete_expenses_for_date(expense_date):
    logging.info(f"{delete_expenses_for_date.__name__} called to delete expense for date: {expense_date}.")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

        # Verify if data is inserted and print success message
        if cursor.rowcount > 0:  # rowcount tells how many rows were affected
            print("Success! Data deleted from database.")
        else:
            print("Error: Data not deleted.")

# Get expense summary for given date range for analytics.
def get_expense_summary(expenses_from_date, expenses_to_date):
    logging.info(f"{get_expense_summary.__name__} called to get expense summary from {expenses_from_date} to {expenses_to_date} date.")
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT category, SUM(amount) as total 
                        FROM expenses WHERE expense_date 
                        BETWEEN %s AND %s
                        GROUP BY category;""", 
                        (expenses_from_date, expenses_to_date)
                    )
        data = cursor.fetchall()
        return data


# if __name__ == "__main__":
    # fetch_all_record()
    # fetch_expenses_for_date("2024-08-05")
    # fetch_expenses_for_date_between("2024-08-05", "2024-09-05")
    # insert_expenses("2025-03-10", 20, "Grocery", "ALDI")
    # delete_expenses_item("40")
    # get_expense_summary("2024-08-05", "2024-09-05")