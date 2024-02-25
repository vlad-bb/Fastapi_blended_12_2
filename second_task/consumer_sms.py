import pika
import json


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='SMS', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received: {message['message']}")
    print(f" [x] {method.delivery_tag}. Повідомлення відправлено за таким номером: {message['phone']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='SMS', on_message_callback=callback)


if __name__ == '__main__':
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Bye bye')
