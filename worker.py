"""
Listen to rabbit and send text messages
"""
import json

import pika
from googlevoice import Voice


def send_sms(message, phone):
    voice = Voice()
    voice.login()

    voice.send_sms(phone, message)


def callback(ch, method, properties, body):
    print(' [x] Received %r' % body)

    data = json.loads(body)

    try:
        send_sms(data['message'], data['phone'])
    except Exception as ex:
        print(' [x] Error: %s' % str(ex))
    else:
        print(' [x] Done')
    ch.basic_ack(delivery_tag = method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )

    channel = connection.channel()

    # TODO: Add support for durable=True
    channel.queue_declare(queue='task_queue')

    channel.basic_consume(
        callback,
        queue='task_queue'
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
