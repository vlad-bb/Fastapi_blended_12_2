import sqlite3
import logging
from tabulate import tabulate


def main(conn, sql_expression):
    c = conn.cursor()
    try:
        c.execute(sql_expression)
        rows = c.fetchall()
        print(tabulate(rows, tablefmt="pretty") + '\n\n')
    except sqlite3.DatabaseError as e:
        logging.error(e)
    finally:
        c.close()


if __name__ == '__main__':
    with sqlite3.connect('db/hw6.sqlite') as conn:
        for i in range(1, 13):
            with open(f'for_sql/{i}.sql', 'r') as file:
                main(conn, file.read())
