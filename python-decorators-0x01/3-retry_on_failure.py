import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('users.db')
        print('with_db_connection decorator start')
        results = func(conn,*args,**kwargs)
        print('with_db_connection decorator end')
        conn.close()
        return results
    return wrapper


""" your code goes here"""
def retry_on_failure(retries,delay):
    def inner(func):
        def wrapper(*args,**kwargs):

            for i in range(retries):
                try:
                    results = func(*args,**kwargs)
                    print('Executed')
                    break
                except:
                    results = []
                    print('Error')

            return results

        return wrapper
    
    return inner



@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ussers")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)