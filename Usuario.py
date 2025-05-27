import pika
import threading
import json

class Usuario:
    def __init__(self, nome, callback_msg):
        self.nome = nome
        self.grupos = set()
        self.callback_msg = callback_msg

        # conexao rabitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # cria exchange tipo topic
        self.exchange = 'chat_exchange'
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        # cria uma fila exclusiva do usuario
        nome_fila = f"fila_{self.nome}"
        result = self.channel.queue_declare(queue=nome_fila,durable=True)
        self.queue_name = result.method.queue

        threading.Thread(target=self.start_consuming, daemon=True).start()

    def entrar_grupo(self, grupo):
        routing_key = f"chat.grupo.{grupo}"
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=routing_key)
        self.grupos.add(grupo)

    def sair_grupo(self,grupo):
        routing_key = f"chat.grupo.{grupo}"
        self.channel.queue_unbind(exchange=self.exchange, queue=self.queue_name, routing_key=routing_key)
        if grupo in self.grupos:
            self.grupos.remove(grupo)

    def enviar_msg(self, grupo, mensagem):
        body = json.dumps({
            'usuario': self.nome,
            'grupo': grupo,
            'mensagem': mensagem
        })
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=f"chat.grupo.{grupo}",
            body=body,
            properties=pika.BasicProperties(delivery_mode=2) #entrega persistente
        )

    def start_consuming(self):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            self.callback_msg(data)
            ch.basic_ack(delivery_tag=method.delivery_tag) #confirmação de recebimento

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=False)
        self.channel.start_consuming()
