from mongoengine import connect, Document, StringField, BooleanField
from dotenv import load_dotenv
import os


load_dotenv()
connect(db='users', host=os.getenv('DB_URI'))


class Contact(Document):
    fullname = StringField(max_length=50)
    email = StringField(max_length=70)
    phone = StringField(max_length=30)
    notify_in = StringField(max_length=15)
    is_notified = BooleanField(default=False)
    meta = {'collection': 'contacts'}

