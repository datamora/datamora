import logging
import logging.config
from bottle import Bottle, debug, run
from bottling.factory import extend
from bottling.persistence import init_db
from bottling.conf import configure


# root app
app = Bottle()


# load and apply settings
settings = configure.from_dir('config')

if settings.has_key('logging'):
    logging.config.dictConfig(settings.get('logging'))

# get our logger going
log = logging.getLogger(__name__)


if settings.has_key('mounts'):
    log.info('mounting apps...')
    extend(app, settings.get('mounts'))


log.info('initializing db...')
init_db()


if __name__ == '__main__':
    if settings.get('server.debug'):
        debug(True)

    host = settings.get('server.host', '0.0.0.0')
    port = settings.get('server.port', '8081')
    reloader = settings.get('server.reloader', False)
    run(app=app, host=host, port=port, reloader=reloader)
