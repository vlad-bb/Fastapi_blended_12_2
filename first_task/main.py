import os
from pymongo import MongoClient
from dotenv import load_dotenv
from redis import StrictRedis
from redis_lru import RedisLRU


client = StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

load_dotenv()
client = MongoClient(os.getenv("DB_URI"))
db = client.hw_8


@cache
def find_by_name(name: str) -> list:
    author_id = db.authors.find_one({'fullname': {'$regex': f'^{name}', "$options": "i"}})
    res = db.quotes.find({'author': author_id['_id']})
    return [el for el in res]


@cache
def find_by_tag(tag: str) -> list:
    res = db.quotes.find({'tags': {'$regex': f'^{tag}', "$options": "i"}})
    return [el for el in res]


@cache
def find_by_tags(tags: list) -> list:
    res = db.quotes.find({'$or': [{'tags': {'$regex': f'^{tag}', "$options": "i"}} for tag in tags]})
    return [el for el in res]


def main():
    while True:
        command = input("Enter command>>>").split(':')
        if command[0] == "name":
            for quote in find_by_name(command[1]):
                print(quote['quote'])
        elif command[0] == "tag":
            for quote in find_by_tag(command[1]):
                print(quote['quote'])
        elif command[0] == "tags":
            for quote in find_by_tags(command[1].split(',')):
                print(quote['quote'])
        elif command[0] == "exit":
            exit()


if __name__ == '__main__':
    main()
