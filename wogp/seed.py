from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

import psycopg2

load_dotenv()


client = MongoClient(os.environ.get('MONGO_URI'))
db = client.test

connection = psycopg2.connect(
    host=os.getenv('PG_HOST'),
    port=os.getenv('PG_PORT'),
    database=os.getenv('PG_NAME'),
    password=os.getenv('PG_PASS'),
    user=os.getenv('PG_USER')
)

cursor = connection.cursor()


authors = db.authors
quotes = db.quotes


def add_tags():
    tags = []
    for quote in quotes.find():
        tags.extend(quote['tags'])
    for tag in set(tags):
        cursor.execute(
            "INSERT INTO noteapp_tag (name) VALUES (%s)",
            (tag,))
    connection.commit()


def add_authors():
    for author in authors.find():
        cursor.execute(
            "INSERT INTO noteapp_author (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s)",
            (author['fullname'], author['born_date'], author['born_location'], author['description'])
        )
    connection.commit()


def add_quotes():
    for quote in quotes.find():
        cursor.execute(
            "SELECT id FROM noteapp_author WHERE fullname = (%s)",
            (authors.find_one({'_id': quote['author']})['fullname'],)
        )
        authors_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO noteapp_quote (quote, author_id, created) VALUES (%s, %s, %s)",
            (quote['quote'], authors_id, datetime.now())
        )
        connection.commit()

        cursor.execute(
            "SELECT id FROM noteapp_quote WHERE quote = (%s)",
            (quote['quote'],)
        )
        quote_id = cursor.fetchone()[0]

        for tag in quote['tags']:
            cursor.execute(
                "SELECT id FROM noteapp_tag WHERE name = (%s)",
                (tag,)
            )
            tag_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO noteapp_quote_tags (quote_id, tag_id) VALUES (%s, %s)",
                (quote_id, tag_id)

            )


if __name__ == '__main__':
    try:
        print('ebanoeit')
        # add_tags()
        # add_authors()
        # add_quotes()
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()

