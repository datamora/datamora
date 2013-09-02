"""
Home Page
=====
"""
from bottle import Bottle


def create_app(config=None, settings=None):
    app = Bottle()

    if config:
        app.config.update(config)

    @app.route('/')
    def index():
        return """
        <h1>Welcome...</h1>
        <p>It's alive!!!</p>
        """

    return app
