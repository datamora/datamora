from bottle import Bottle, template, request
import bottle
from bottle.ext.factory import extend
import yaml


app = Bottle()
with open('config/settings.yml') as f:
    settings = yaml.load(f)

    print settings
    extend(app, settings['mounts'])

    app.config.load_dict(config)


@app.get('/hello/<name>')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.get('/debug')
def debug():
    return template('<pre>{{config}}</pre>', config=request.app.config)


if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app, host="0.0.0.0", port=8081, reloader=True)
