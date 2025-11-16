import sqlite3 

class DatabaseConnection:

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        return cursor
    
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

age = 25
with DatabaseConnection() as cursor:
    cursor.execute(f"SELECT * FROM users WHERE age > {age}")
    print(cursor.fetchall())