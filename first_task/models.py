from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
from dotenv import load_dotenv
import os


load_dotenv()
connect(db='hw_8', host=os.getenv('DB_URI'))


class Author(Document):
    fullname = StringField(required=False, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {'collection': 'authors'}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    quote = StringField()
    meta = {'collection': 'quotes'}
