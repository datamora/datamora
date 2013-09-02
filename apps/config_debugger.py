"""
Debug
=====

Loads and dsiplay config info that is used by running app.
"""
from bottle import Bottle


def create_app(config=None, settings=None, host_app=None):
    app = host_app if host_app else Bottle()

    if config:
        app.config.update(config)

    @app.route('/')
    def index():
        return app.config

    return app
