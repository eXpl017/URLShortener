import mariadb
from db_config import db_conn
from b62 import b62_encode

START_INCREMENT=21000000

conn, cursor = None, None

def _get_conn():
    global conn, cursor
    conn = db_conn()
    cursor = conn.cursor()
    return (conn, cursor)

def _close_conn(conn):
    try:
        conn.close()
    except mariadb.Error as e:
        print("Couldn't close connection.")
        print(f"Error: {e}")

def create_table():

    ## get conn and cursor

    conn, cursor = _get_conn()

    ## creating url_info table

    table_name = "url_info"
    table_cols = [
            "num INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY",
            "tiny_url CHAR(5) BINARY NOT NULL",
            "long_url TEXT NOT NULL",
            "c_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ]
    create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(table_cols)})"
    alter_stmt = f"ALTER TABLE {table_name} AUTO_INCREMENT={START_INCREMENT}"

    try:
        cursor.execute(create_stmt)
        cursor.execute(alter_stmt)
        conn.commit()
        print("Table created or already exists.")

    except (mariadb.DatabaseError, mariadb.OperationalError) as db_err:
        print(f"DBError/OpError occured: {db_err}")
        if conn: conn.rollback()

    except mariadb.Error as e:
        print(f"Error occured: {e}")
        if conn: conn.rollback()

    finally: _close_conn(conn)

def insert_value(long_url):

    ## get conn and cursor

    conn, cursor = _get_conn()

    ## insert values in db

    conn.autocommit = False

    placeholder = "#####"
    insert_stmt = "INSERT INTO url_info (tiny_url, long_url) VALUES (?,?)"
    update_stmt = "UPDATE url_info SET tiny_url=? WHERE num=?"
    insert_data = (placeholder, long_url)

    try:
        cursor.execute(insert_stmt, insert_data)
        num = cursor.lastrowid

        tiny = b62_encode(num)
        update_data = (tiny, num)

        cursor.execute(update_stmt, update_data)
        conn.commit()

        return tiny

    except mariadb.Error as e:
        print(f'Failed to execute or commit, rolling back.')
        if conn: conn.rollback()

    finally: _close_conn(conn)

def get_long_url(tiny_url):

    ## get conn and cursor

    conn, cursor = _get_conn()

    ## fetch info

    select_stmt = "SELECT long_url, c_date FROM url_info WHERE tiny_url=?"
    try:
        cursor.execute(select_stmt, (tiny_url,))
        info = cursor.fetchone()
        if info:
            return(info)
        else:
            raise LookupError('No corressponding URL found!')

    except LookupError as le:
        print(f'Error: {le}')

    except mariadb.Error as e:
        print(f'Error occured: {e}')

    finally: _close_conn(conn)


# conn, cursor = get_conn()
# create_table(conn,cursor)
# insert_value(conn, cursor, "lmao")
# insert_value(conn, cursor, "sdfghuiop")
# insert_value(conn, cursor, "lasdtqviv")
# get_long_url('1q748')
# get_long_url(cursor, '1q73L')
# get_long_url(cursor, '1q73K')
