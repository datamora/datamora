"""
Debug
=====

Loads and dsiplay config info that is used by running app.
"""
from bottle import Bottle


def create_app(custom_config=None, host_app=None):
    app = host_app if host_app else Bottle()

    if custom_config:
        app.config.update(custom_config)

    @app.route('/')
    def index():
        return app.config

    return app
