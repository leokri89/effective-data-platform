from confluent_kafka import Producer
from faker import Faker
import json
import time

# Configurações do Kafka
topic = 'produtos'

# Configurações do produtor
conf = {'bootstrap.servers': 'kafka1:9092,kafka2:9092,kafka3:9092'}

# Criação do produtor Kafka
producer = Producer(**conf)

# Função para enviar mensagens ao Kafka


def send_message():
    fake = Faker()

    # Geração de dados fake
    # data = {
    #     'id': fake.uuid4(),
    #     'produto': fake.word(),
    #     'quantidade': fake.random_int(min=1, max=100),
    #     'preco': fake.random_int(min=1.0, max=100.0),
    # }
    
    i = 0
    while i < 50000:
        data = {
            'id_cliente': 1000 + i,
            'id_produto': 405150 + i,
            'produto': fake.word(),
            'quantidade': fake.random_int(min=1, max=100),
            'preco': fake.random_int(min=1.0, max=100.0),
        }
        i += 1

    # Conversão do dicionário para formato JSON
        message = json.dumps(data).encode('utf-8')
    
        # Envio da mensagem ao tópico Kafka
        producer.produce(topic, message)
    
        # Aguarda confirmação de entrega da mensagem
        producer.flush()
        print(f"Mensagem enviada: {message}")


if __name__ == '__main__':
    
    send_message()
            
    # try:
    #     # Loop para enviar mensagens continuamente
    #     while True:
    #         send_message()
    #         # Aguarda 1 segundo entre as mensagens
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     # Encerra o produtor Kafka
    #     producer.flush()