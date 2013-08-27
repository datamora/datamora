class TimeSeriesController(object):
    def __init__(self, request, db):
        self.request = request
        self.db = db

    def get_all_streams(self):
        streams = []
        for stream in db.query(Stream).all():
            streams.append({'id': stream.id, 'key': stream.key, 'name': stream.name})

    def get_stream_by_key(self, key):
        streams = []
        stream = self.db.query(Stream).filter_by(key=key).first()
        streams.append(stream_to_resource(stream))
        return streams

def stream_to_resource(stream):
    return {'id': stream.id, 'key': stream.key, 'name': stream.name}