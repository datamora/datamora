from .models import Stream


class TimeSeriesController(object):
    def __init__(self, db):
        self._db = db

    def get_all_streams(self):
        streams = []
        for stream in self._db.query(Stream).all():
            streams.append({'id': stream.id, 'key': stream.key, 'name': stream.name})
        return streams

    def get_stream_by_key(self, key):
        streams = []
        stream = self._db.query(Stream).filter_by(key=key).first()
        streams.append(stream_to_dto(stream))
        return streams

    def get_stream_by_id(self, id):
        stream = self._db.query(Stream).filter_by(id=id).first()
        if stream:
            return stream_to_dto(stream) 
        return None

    def create_stream(self, stream_dto):
        stream = Stream(key=stream_dto['key'], name=stream_dto['name'], description=stream_dto['description'])
        self._db.add(stream)
        self._db.commit()
        return stream.id


def stream_to_dto(stream):
    return {'id': stream.id, 'key': stream.key, 'name': stream.name}

