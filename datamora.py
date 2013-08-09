from bottle import Bottle
import bottle
from bottle.ext.factory import extend


app = Bottle()

# extend(app, settings.MOUNTS)

if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app, host="0.0.0.0", port=80, reloader=True)
