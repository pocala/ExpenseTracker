
from mysql.connector import MySQLConnection, Error #importing MySQL connection components
from config import read_config #import the method from config.py

#help(mysql.connector)

def connect(config):
    # Connect to MySQL Database
    # Initialize a variable to hold the database connection
    conn = None
    try:
        print("Connecting to MySQL database..")
        conn = MySQLConnection(**config)
        if conn.is_connected():
            print("Connection established.")
        else:
            print("Connection has failed.")
    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connection is closed.")

def create_expense_table(conn: MySQLConnection): # Add a type hint MySQLConnection
    # Create a cursor object
    cursor = conn.cursor()
    
    # SQL command to create table if it does not exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
    Trans_id INT AUTO_INCREMENT PRIMARY KEY,
    Date VARCHAR(10),
    Category VARCHAR(20),
    Description VARCHAR(20),
    Amount INT
    )""")
    conn.commit()
    cursor.close()

def insert_expense(date, category, description, amount):
    
    query = "INSERT INTO expenses(date, category, description, amount) " \
            "VALUES(%s, %s, %s, %s)"
    args = (date, category, description, amount) # Arguments that is parsed into the function
    trans_id = None
    try:
        config = read_config() # Gets the database config such as port, password, etc
        with MySQLConnection(**config) as conn: # **config unpacks the dict into keyword arguments
            with conn.cursor() as cursor: # A cursor is an iterator that allows SQL command execution & retrieve data from databases
                cursor.execute(query, args) # Execute function requires the query and args, where query is the commands and args are the variable inputs
                trans_id = cursor.lastrowid
                print("Expense saved successfully")
            conn.commit() # Commit the changes made
        return trans_id
    except Error as error:
        print(error)

def delete_expense(expense_id):
    # Read the database config
    config = read_config()
    query = "DELETE FROM expenses WHERE trans_id = %s"
    data = (expense_id, )
    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                affected_rows = cursor.rowcount # Get the number of affected rows
                print("Expense deleted succesfully")
            conn.commit()
    except Error as error:
        print(error)
    return affected_rows

def view_expenses(): # Function to return all rows from MySQL database
    config = read_config()
    expenses_list = [] # Initialize an empty list
    column_names = []
    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM expenses")
                rows = cursor.fetchall()
                column_names = [i[0] for i in cursor.description] # There are 7 different item types, [0] returns the names. Each column has a tuple of 7 elements
                for row in rows:
                    expenses_list.append(row) # Add each row to the list
    except Error as error:
        print(error)
    return expenses_list, column_names

def get_expense_info(trans_id_input):
    config = read_config()
    expense_info = [] # List to hold the expense info based on trans_id input to this function
    query = """SELECT * FROM expenses WHERE Trans_id = %s"""
    data = (trans_id_input,)
    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                row = cursor.fetchone()
                if row is None:
                    return None 
                for i in row:
                    expense_info.append(i)
                conn.commit()
    except Error as error:
        print(error)
    return expense_info

def edit_expenses(transactionID, dateInput, categoryInput, descriptionInput, amountInput):
    config = read_config()
    query = """UPDATE expenses
    SET Date = %s,
    Category = %s,
    Description = %s,
    Amount = %s
    WHERE Trans_ID = %s"""
    
    data = (dateInput, categoryInput, descriptionInput, amountInput, transactionID) # To input data into the query
    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                conn.commit()
    except Error as error:
        print(error)
    

if __name__ == "__main__": # To ensure code is executed when run directly
    '''config = read_config()
    conn = MySQLConnection(**config)
    create_expense_table(conn)'''
    e = get_expense_info(3)
    print(e)
    
    