import yaml
from bottle import Bottle, debug, run
from bottling.factory import extend


app = Bottle()

with open('config/settings.yml') as f:
    settings = yaml.load(f)

    print settings
    extend(app, settings['mounts'])


if __name__ == '__main__':
    debug(True)
    run(app=app, host="0.0.0.0", port=8081, reloader=True)
