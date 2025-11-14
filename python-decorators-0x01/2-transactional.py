import sqlite3 
import functools

"""your code goes here"""
def with_db_connection(func):
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('users.db')
        print('with_db_connection decorator start')
        results = func(conn,*args,**kwargs)
        print('with_db_connection decorator end')
        conn.close()
        return results
    return wrapper

def transactional(func):
    def wrapper(*args,**kwargs):
        print('transactional decorator start')
        conn = args[0]
        try:
            results = func(*args,**kwargs)
            conn.commit()
        except:
            print('error')
            conn.rollback()
        print('transactional decorator end')
        return results

    return wrapper

@with_db_connection 
@transactional
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    print('Main function execution')
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')