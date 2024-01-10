from confluent_kafka import Producer, Consumer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

class KafkaRepository:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _get_admin_client(self):
        client = AdminClient({
            'bootstrap.servers': f'{self.host}:{self.port}'
        })
        return client
    
    def _get_producer_client(self):
        client = Producer({
            'bootstrap.servers': f'{self.host}:{self.port}'
        })
        return client

    def _get_consumer_client(self):
        client = Consumer({
            'bootstrap.servers': f'{self.host}:{self.port}',
            'group.id': 'pythongroup',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        })
        return client

    def list_topics(self):
        client = self._get_admin_client()
        return client.list_topics().topics
    
    def is_topic_exists(self, topic):
        topic_metadata = self.list_topics()
        if topic_metadata.get(topic) is None:
            return False
        else:
            return True
        
    def create_topic(self, topic):
        retention_minutes = 1
        if not self.is_topic_exists(topic):
            client = self._get_admin_client()
            new_topic = NewTopic(topic,
                                num_partitions=1, 
                                replication_factor=1, 
                                config={
                                    'retention.ms': str(retention_minutes * 60 * 1000),
                                    'cleanup.policy': 'delete',
                                    'delete.retention.ms': str(retention_minutes * 60 * 1000),
                                    'file.delete.delay.ms': str(retention_minutes * 60 * 1000),
                                    'min.cleanable.dirty.ratio': '0.01',
                                    'segment.ms': str(retention_minutes * 60 * 1000),
                                    'min.insync.replicas': '1',
                                    'retention.bytes': '-1'
                                    }
                                )
            client.create_topics([new_topic])
            print(f'Tópico {topic} criado com sucesso!')
            return client
        else:
            print(f'Tópico {topic} já existe!')

    def delete_topic(self, topic):
        if self.is_topic_exists(topic):
            client = self._get_admin_client()
            client.delete_topics([topic], operation_timeout=3)
            print(f'Tópico {topic} deletado com sucesso!')
            return client
        else:
            print(f'Tópico {topic} não existe!')

    def list_consumer_groups(self):
        client = self._get_admin_client()
        consumer_groups = client.list_consumer_groups()
        return consumer_groups.result().valid

    def delete_consumer_groups(self, group_id):
        groups = self.list_consumer_groups()
        if group_id in groups:
            client = self._get_admin_client()
            client.delete_consumer_group(group_id)
            print(f"Consumer group {group_id} deleted")
            return client
        print(f"Consumer group {group_id} not found!")

    def publish_one_text_messages(self, topic, message):
        if self.is_topic_exists(topic):
            if isinstance(message, str):
                producer = self._get_producer_client()
                producer.produce(topic, message.encode('utf-8'))
                print(f'Mensagem enviada: {message}!')
                producer.flush()
                return
            else:
                print('Tipo de mensagem incorreto, apenas str!')
                return
        else:
            print(f'Topico {topic} não existe!')
            return

    def publish_batch_text_messages(self, topic, messages):
        if self.is_topic_exists(topic):
            if isinstance(messages, list):
                producer = self._get_producer_client()
                for message in messages:
                    if isinstance(messages, str):
                        producer.produce(topic, message.encode('utf-8'))
                        producer.produce(topic, message.encode('utf-8'))
                producer.flush()
                return
            else:
                print('Tipo de mensagem incorreto, apenas list!')
                return
        else:
            print(f'Topico {topic} não existe!')
            return

    def _assignment_callback(self, consumer, partitions):
        for p in partitions:
            p.offset=-2
            consumer.assign(partitions)
            print(f'Assigned to {p.topic}, partition {p.partition}')

    def consume_messages(self, topic):
        try:
            consumer = self._get_consumer_client()
            consumer.subscribe([topic], on_assign=self._assignment_callback)
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                print(f'Mensagem recebida: {msg.value().decode("utf-8")}')
                consumer.commit(msg)
        except KeyboardInterrupt:
            print('Canceled by user!')
        finally:
            consumer.close()