from models import Author, Quote
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os


load_dotenv()
client = MongoClient(os.getenv("DB_URI"))
db = client.hw_8


def wipe_db():
    db.authors.drop()
    db.quotes.drop()


def dump_authors():
    with open('../data/authors.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for el in data:
            author = Author(fullname=el['fullname'],
                            born_date=el['born_date'],
                            born_location=el['born_location'],
                            description=el['description'])
            author.save()


def dump_quotes():
    with open('../data/quotes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for el in data:
            author, *_ = Author.objects(fullname=el['author'])
            quote = Quote(quote=el['quote'],
                          tags=el['tags'],
                          author=author)
            author.save()
            quote.save()


if __name__ == '__main__':
    # wipe_db()
    dump_authors()
    dump_quotes()
