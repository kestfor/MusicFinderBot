import json


class TrackTask:

    KEY = "track_task"
    KAFKA_TOPIC = "track_task"

    def __init__(self, track_id: str, title: str, artist: str, duration: int, chat_id):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.track_id = track_id
        self.chat_id = chat_id


class TrackEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TrackTask):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
