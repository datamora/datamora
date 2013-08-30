import yaml
from bottle import Bottle, debug, run
from bottling.factory import extend

import logging
logging.basicConfig(level=logging.INFO)


app = Bottle()

with open('config/settings.yml') as f:
    settings = yaml.load(f)
    extend(app, settings['mounts'])


logging.debug('here')
logging.warning('bad')


if __name__ == '__main__':
    debug(True)
    run(app=app, host="0.0.0.0", port=8081, reloader=True)
