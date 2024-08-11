import json

from confluent_kafka import Producer, KafkaError, KafkaException

from communication_service.track_task import TrackTask, TrackEncoder


class Sender:
    config = {
        'bootstrap.servers': 'localhost:9092',
    }

    @staticmethod
    def _delivery_report_log(err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
            raise KafkaException("delivery failed")
        else:
            print(f'Message delivered with topic "{msg.topic()}" to [{msg.partition()}]')

    def __init__(self):
        self._producer = Producer(Sender.config)

    def send_task(self, topic: str, track_task: TrackTask):
        self._producer.produce(topic=topic, key=str(track_task.chat_id),
                               value=f"new track task from user {track_task.chat_id}",
                               headers={TrackTask.KEY: json.dumps(track_task, cls=TrackEncoder).encode('utf-8')},
                               on_delivery=self._delivery_report_log)
        self._producer.flush()
