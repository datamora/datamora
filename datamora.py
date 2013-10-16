import logging
import logging.config

from sqlalchemy import create_engine

from bottle import Bottle, debug, run
from bottling.config import load_settings

from apps import index, config_debugger, fois


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


    # setup data access
    engine = None
    if 'sqlalchemy' in settings:
        logger.info('Setting up data access...')
        engine_config = settings['sqlalchemy']['master']
        engine = create_engine(engine_config['url'], echo=engine_config['echo'])


    # create root app and mount sub apps
    logger.info('Composing apps...')

    app = index.app

    app.mount('/debug', config_debugger.create_app())

    app.mount('/streams', fois.app)
    fois.init(engine)
    

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
