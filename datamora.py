from bottle import Bottle, template, request
import bottle
from bottle.ext.factory import extend
import yaml


app = Bottle()
with open('config/settings.yml') as f:
    settings = yaml.load(f)

    print settings
    extend(app, settings['mounts'])


@app.get('/hello/<name>')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name) 


if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app, host="0.0.0.0", port=8081, reloader=True)
