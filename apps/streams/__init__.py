"""
Streams
========

Stores basic time-series events in collections (streams).

Stream:
    - name
    - description

Event:
    - title
    - timestamp (auto set if not available)
"""
from bottle import Bottle, view


def create_app(custom_config=None, host_app=None):
    app = host_app if host_app else Bottle()
    db = {'foo':[], 'bar': ['1','2','3']}

    @app.get('/')
    @view('index')
    def get_streams():
        return {'streams': db.keys()}

    @app.get('/stream/<name>')
    def get_stream(name):
        return db[name]

    @app.post('/stream/<name>/events/')
    def add_event(name):
        db[name] = []

    return app