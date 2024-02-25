import pika
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
client = MongoClient(os.getenv("DB_URI"))
db = client.users


def get_users_data():
    return [el for el in db.contacts.find({}, {'_id': 0})]


def publish_contact(ch):
    data = get_users_data()
    for user in data:
        if user['notify_in'] == 'SMS':
            user.update({'message': 'Дуже важливе помідомлення на SMS'})
        else:
            user.update({'message': 'Дуже важливе помідомлення на EMAIL'})
        ch.basic_publish(exchange='task_mock',
                         routing_key=user['notify_in'],
                         body=json.dumps(user, ensure_ascii=False).encode(),
                         properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672,
                                                                   credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='task_mock', exchange_type='direct')

    channel.queue_declare(queue='EMAIL', durable=True)
    channel.queue_bind(exchange='task_mock', queue='EMAIL')

    channel.queue_declare(queue='SMS', durable=True)
    channel.queue_bind(exchange='task_mock', queue='SMS')

    publish_contact(channel)
    connection.close()


if __name__ == '__main__':
    main()
    # print(get_users_data())
