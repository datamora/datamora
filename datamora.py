import logging
import logging.config
from bottle import Bottle, debug, run
from bottling.config import load_settings
from bottling.persistence import get_datastores, setup_datastores, init_datastores
from bottling.factory import mount_all

from pprint import pprint as pp


SERVER_DEFAULT_CONFIG = dict(host='localhost', port=8081, reloader=False, debug=False)


datastores = None


# load settings
load_settings('config')
from bottling.config import settings


# setup logging
if 'logging' in settings:
    logging.config.dictConfig(settings.get('logging'))

log = logging.getLogger(__name__)


# setup datastores
if 'datastore' in settings:
    log.info('setting up datastores....')
    # setup_datastores(settings['datastores'])
    datastores = get_datastores(settings['datastore'])


# create root app and mount sub apps
root = app = Bottle()
if 'app' in settings:
    log.info('mounting apps...')
    extend(root, settings.get('app'), settings)


# initialize datastores
if datastores:
    log.info('initializing datastores...')
    datastores.init()


if __name__ == '__main__':
    server_config = SERVER_DEFAULT_CONFIG.copy()
    print settings
    if 'server' in settings:
        server_config.update(settings.get('server', {}))

    if server_config['debug']:
        debug(True)

    run(app=app, host=server_config['host'], port=server_config['port'], reloader=server_config['reloader'])
