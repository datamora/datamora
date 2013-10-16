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
import os
import logging
from bottle import Bottle, view, request, response, HTTPError, TEMPLATE_PATH
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine

from .models import Base
from .controllers import TimeSeriesController


logger = logging.getLogger(__name__)

app = Bottle()
    
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
    c = TimeSeriesController(db)

    stream = c.get_stream_by_id(id)
    if not stream:
        return HTTPError(404, 'Stream not found.')
    return stream


def _stream_dto_from_request(request):
    key = request.POST.get('key')
    name = request.POST.get('name')
    description = request.POST.get('description')
    return dict(key=key, name=name, description=description)


def init(engine=None, plugin=None):
    # install sa plugin and initialise db
    logger.info('Initialising app...')

    _install_plugin(engine, plugin)
    _register_views()


def _install_plugin(engine=None, plugin=None):
    if not engine:
        logger.info('Creating in-memory db...')
        engine = create_engine('sqlite:///:memory:', echo=False)
    if not plugin:
        logger.info('Creating SQLAlchemy Plugin...')
        plugin_config = dict(keyword='db', create=False, commit=True, use_kwargs=True)
        plugin = sqlalchemy.Plugin(engine, **plugin_config)

    app.install(plugin)
    Base.metadata.create_all(engine)


def _register_views():
    root_path = os.path.dirname(__file__)
    views_dir = os.path.abspath(os.path.join(root_path, 'views'))
    logger.info('Registering views dir: %s' % views_dir)
    TEMPLATE_PATH.append(views_dir)
        
