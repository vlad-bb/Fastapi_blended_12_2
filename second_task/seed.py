from models import Contact
from pymongo import MongoClient
from dotenv import load_dotenv
from mimesis import Person, Locale
from random import choice
import os


person = Person(Locale.UK)

load_dotenv()
client = MongoClient(os.getenv("DB_URI"))
db = client.users


def wipe_db():
    db.contacts.drop()


def fill_users_collection():
    for _ in range(20):
        contact = Contact(fullname=person.full_name(),
                          email=person.email(),
                          phone=person.phone_number(),
                          notify_in=choice(['SMS', 'EMAIL'])
                          )
        contact.save()


if __name__ == '__main__':
    # wipe_db()
    fill_users_collection()
