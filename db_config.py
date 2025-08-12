import mariadb
import sys

def db_conn():

    conn = None

    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': '<user-here>',
        'password': '<password-here>',
        'database': 'url_shortener'
    }

    try:
        print("Connecting to DB.")
        conn = mariadb.connect(**db_config)
        print("Connection successful!")
    except mariadb.Error as e:
        print(f"Error occured: {e}")
        sys.exit(1)

    return conn
