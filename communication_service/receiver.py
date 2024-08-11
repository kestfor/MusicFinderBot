from confluent_kafka import Consumer, KafkaException
import json
from types import SimpleNamespace
from communication_service.track_task import TrackTask


class Receiver:
    config = {
        'bootstrap.servers': 'localhost:9092',  # Список серверов Kafka
        'group.id': 'finderGroup',  # Идентификатор группы потребителей
        'auto.offset.reset': 'latest'  # Начальная точка чтения ('earliest' или 'latest')
    }

    def __init__(self, topic: str):
        self._consumer = Consumer(Receiver.config)
        self._consumer.subscribe([topic])

    def close(self):
        self._consumer.close()

    def receive(self) -> TrackTask:
        msg = self._consumer.poll()

        if msg.error():  # обработка ошибок
            raise KafkaException(msg.error())
        else:
            headers = msg.headers()
            key, data = headers[0]

            data = data.decode('utf-8')
            task = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            return task
