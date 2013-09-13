from sqlalchemy import create_engine
from bottle.ext import sqlalchemy


def create_engine(self, config):
    return create_engine(config['dsn'], echo=config['echo'])

def create_plugin(engine, config):
    sqlalchemy.Plugin(engine, **config)
