import logging
import logging.config

from bottle import Bottle, debug, run

from bottling.config import load_settings
from bottling.persistence import get_datastores, setup_datastores, init_datastores
from bottling.factory import builder, ConfigBasedResolver


# =========================================================
# Launcher
# =========================================================

def main(config_dir='config'):

    # load settings
    settings = load_settings(config_dir)

    # setup logging
    if 'logging' in settings:
        logging.config.dictConfig(settings.get('logging'))

    logger = logging.getLogger(__name__)
    logger.info('Settings loaded, bootstrapping...')

    # setup datastores
    datastores = None
    if 'datastores' in settings:
        logger.info('Setting up datastores...')
        # setup_datastores(settings['datastores'])
        datastores = get_datastores(settings['datastores'])

    # create root app and mount sub apps
    app = None
    if 'apps' in settings:
        logger.info('Composing apps...')
        resolver = ConfigBasedResolver(datastores=datastores)
        app = builder.build(settings.get('apps'), resolver)

    # configure server and run
    server_config = dict(host='localhost', port=8081, reloader=False, debug=False)
    if 'server' in settings:
        server_config.update(settings.get('server', {}))

    if server_config['debug']:
        debug(True)
    logger.info('Starting server...')

    run(app=app, host=server_config['host'], port=server_config['port'], reloader=server_config['reloader'])



# =========================================================
# CLI 
# =========================================================

if __name__ == '__main__':
    main()
