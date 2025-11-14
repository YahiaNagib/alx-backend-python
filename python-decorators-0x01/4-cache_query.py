import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('users.db')
        print('with_db_connection decorator start')
        results = func(conn,*args,**kwargs)
        print('with_db_connection decorator end')
        conn.close()
        return results
    return wrapper

"""your code goes here"""
def cache_query(func):
    def wrapper(*args,**kwargs):
        query = kwargs['query']
        if query in query_cache:
            print('Second Time')
            return query_cache[query]
        else:
            print('First Time')
            query_cache[query] = func(*args,**kwargs)
            return query_cache[query]
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(query_cache)