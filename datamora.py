import logging
import logging.config
from bottle import Bottle, debug, run
from bottling.config import load_settings



# =========================================================
# Bootstrap
# =========================================================

SERVER_DEFAULT_CONFIG = dict(host='localhost', port=8081, reloader=False, debug=False)

datastores = None

# load settings
load_settings('config')
from bottling.config import settings

# setup logging
if 'logging' in settings:
    logging.config.dictConfig(settings.get('logging'))

log = logging.getLogger(__name__)



# =========================================================
# Initialize
# =========================================================

from bottling.persistence import get_datastores, setup_datastores, init_datastores
from bottling.factory import builder

# setup datastores
if 'datastore' in settings:
    log.info('setting up datastores....')
    # setup_datastores(settings['datastores'])
    datastores = get_datastores(settings['datastore'])


# create root app and mount sub apps
app = None
if 'apps' in settings:
    log.info('composing apps...')
    app = builder.build(settings.get('apps'))


# initialize datastores
if datastores:
    log.info('initializing datastores...')
    datastores.init()



# =========================================================
# Launch
# =========================================================

if __name__ == '__main__':
    server_config = SERVER_DEFAULT_CONFIG.copy()
    if 'server' in settings:
        server_config.update(settings.get('server', {}))

    if server_config['debug']:
        debug(True)

    run(app=app, host=server_config['host'], port=server_config['port'], reloader=server_config['reloader'])
