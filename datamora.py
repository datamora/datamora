import logging
import logging.config
from bottle import Bottle, debug, run
from bottling.factory import extend
from bottling.persistence import init_db
from bottling.config import configure


SERVER_DEFAULT_CONFIG = dict(host='localhost', port=8081, reloader=False, debug=False)

# load and apply settings
settings = configure.from_dir('config')

# setup logging
if 'logging' in settings:
    logging.config.dictConfig(settings.get('logging'))

log = logging.getLogger(__name__)

# create root app and mount sub apps
root = app = Bottle()
if 'apps' in settings:
    log.info('mounting apps...')
    extend(root, settings.get('apps'), settings)

# initialize database
log.info('initializing db...')
init_db()


if __name__ == '__main__':
    server_config = SERVER_DEFAULT_CONFIG.copy()
    if 'server' in settings:
        server_config.update(settings.get('server', {}))

    if server_config['debug']:
        debug(True)

    run(app=app, host=server_config['host'], port=server_config['port'], reloader=server_config['reloader'])
