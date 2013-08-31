from .models import Stream


class TimeSeriesController(object):
    def __init__(self, db):
        self.db = db

    def get_all_streams(self):
        streams = []
        for stream in self.db.query(Stream).all():
            streams.append({'id': stream.id, 'key': stream.key, 'name': stream.name})
        return streams

    def get_stream_by_key(self, key):
        streams = []
        stream = self.db.query(Stream).filter_by(key=key).first()
        streams.append(stream_to_resource(stream))
        return streams

    def create_stream(self, stream_dto):
        stream = Stream(key=stream_dto['key'], name=stream_dto['name'], description=stream_dto['description'])
        self.db.add(stream)
        self.db.commit()
        return stream.id


def stream_to_resource(stream):
    return {'id': stream.id, 'key': stream.key, 'name': stream.name}

