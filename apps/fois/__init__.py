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
from bottle import Bottle, view, request, response, HTTPError
from bottling.persistence import storage
from .controllers import TimeSeriesController

import logging
logger = logging.getLogger(__name__)


def create_app(custom_config=None, host_app=None):
    app = host_app if host_app else Bottle()
    app.install(storage)

    @app.get('/')
    @view('index')
    def get_streams(db):
        c = TimeSeriesController(db)

        key = request.query.key or None

        if key:
            return dict(streams = [c.get_stream_by_key(key)])
        else: 
            return dict(streams = c.get_all_streams())

    @app.post('/')
    def post_stream(db):
        c = TimeSeriesController(db)
        stream_dto = _stream_dto_from_request(request)
        id = c.create_stream(stream_dto)
        response.status = '201 Created'
        response.set_header('Location', '/stream/%s' % id)

    @app.get('/stream/<id>')
    def get_stream(id, db):
        stream = db.query(Stream).filter_by(id=id).first()
        if stream:
            return _stream_to_resource(stream)
        return HTTPError(404, 'Stream not found.')

    return app


def _stream_dto_from_request(request):
    key = request.POST.get('key')
    name = request.POST.get('name')
    description = request.POST.get('description')
    return dict(key=key, name=name, description=description)


