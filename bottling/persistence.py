from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from bottle.ext import sqlalchemy

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

storage = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=False, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=True # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    session = storage.create_session()
    if not session.bind:
        session.bind = engine
    return session