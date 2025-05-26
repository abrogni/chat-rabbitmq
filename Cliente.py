# cliente.py

import pika
import threading
import json

class ChatClient:
    def __init__(self, username, message_callback):
        self.username = username
        self.groups = set()
        self.message_callback = message_callback

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.exchange = 'chat_exchange'
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue

        threading.Thread(target=self.start_consuming, daemon=True).start()

    def join_group(self, group):
        routing_key = f"chat.group.{group}"
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=routing_key)
        self.groups.add(group)

    def send_message(self, group, message):
        body = json.dumps({
            'sender': self.username,
            'group': group,
            'message': message
        })
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=f"chat.group.{group}",
            body=body
        )

    def start_consuming(self):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            self.message_callback(data)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
