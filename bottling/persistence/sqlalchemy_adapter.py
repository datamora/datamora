from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from bottle.ext import sqlalchemy


class SQLAlchemyDatastore(object):
    def __init__(self, config):
        engine_config = config['engine']
        plugin_config = config['plugin']

        self.Base = declarative_base()
        self.engine = self.create_engine(engine_config)
        self.plugin = self.create_plugin(self.engine, plugin_config)

    def init(self):
        self.Base.metadata.create_all(self.engine)

    def db(self):
        session = self.plugin.create_session()
        if not session.bind:
            session.bind = self.engine
        return session

    def create_plugin(self, engine, config):
        return sqlalchemy.Plugin(engine, **config)

    def create_engine(self, config):
        return create_engine(config['dsn'], echo=config['echo'])


def create_datastore(config):
    return SQLAlchemyDatastore(config)