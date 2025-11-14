import sqlite3 

class DatabaseConnection:

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        return cursor
    
    def __exit__(self, type, value, traceback):
        self.conn.close()

with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())