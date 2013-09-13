"""
Home Page
=====
"""
from bottle import Bottle


DEFAULT_SETTINGS = {
    "title": "Welcome!!!",
    "message": "It's alive!!!!!!!"
}

app = Bottle()
app.config.update(DEFAULT_SETTINGS)

@app.route('/')
def index():
    return """
    <h1>{{title}}</h1>
    <p>{{message}}</p>
    """ % (app.config['title'], app.config['message'])
