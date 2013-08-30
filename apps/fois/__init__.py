"""
Fois (times)
=============

Captures basic time-series events in streams.

Stream:
    - key
    - name
    - description

Event:
    - timestamp (auto set if not available)
    - value (int)
    - note (string, 256)

Entry:
    - timestamp (auto set if not available)
    - note (text)
"""
from bottle import Bottle, view, request, HTTPError
from bottling.db import persistence
from .models import Stream, Event, Entry

import logging
logger = logging.getLogger(__name__)


def create_app(custom_config=None, host_app=None):
    app = host_app if host_app else Bottle()
    app.install(persistence)

    @app.get('/')
    @view('index')
    def get_streams(db):
        streams = []
        key = request.query.key or None
        if key:
            stream = db.query(Stream).filter_by(key=key).first()
            streams.append({'id': stream.id, 'key': stream.key, 'name': stream.name})
        else: 
            streams = [_stream_to_resource(stream) for stream in db.query(Stream).all()]
        
        return dict(streams=streams)

    @app.get('/stream/<id>')
    def get_stream(id, db):
        stream = db.query(Stream).filter_by(id=id).first()
        if stream:
            return _stream_to_resource(stream)
        return HTTPError(404, 'Stream not found.')

    @app.post('/stream/<id>/events/')
    def add_event(id, db):
        stream = _stream_from_request(request)
        db.add(stream)

    return app


def _stream_to_resource(stream):
    return dict(id=stream.id, key=stream.key, name=stream.name)

def _stream_from_request(request):
    key = request.POST.get('key')
    name = request.POST.get('name')
    description = request.POST.get('description')
    return Stream(key=key, name=name, description=description)

