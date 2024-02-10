import sqlite3
import logging


def create_table(conn, sql_expression):
    c = conn.cursor()
    try:
        c.executescript(sql_expression)
        conn.commit()
    except sqlite3.Error as e:
        logging.error(e)
        conn.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    with sqlite3.connect('db/hw6.sqlite') as conn:
        with open('for_sql/create-tables.sql') as f:
            create_table(conn, f.read())
