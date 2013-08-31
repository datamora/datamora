import datetime
from sqlalchemy import Column, Integer, Sequence, String, Text, DateTime
from bottling.persistence import Base


class Stream(Base):
    __tablename__ = 'streams'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    key = Column(String(255), unique=True)
    name = Column(String(255))
    description = Column(Text)

    def __init__(self, key, name=None, description=None):
        self.key = key
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Stream('%d', '%s', '%s')>" % (self.id, self.key, self.name)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    value = Column(Integer)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    note = Column(String(255))

    def __init__(self, value, ts=None, note=None):
        self.value = value
        self.ts = ts
        self.note = note

    def __repr__(self):
        return "<Event('%d', '%s', '%s')>" % (self.id, self.ts, self.value)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    note = Column(Text)

    def __init__(self, ts=None, note=None):
        self.ts = ts
        self.note = note

    def __repr__(self):
        return "<Entry('%d', '%s', '%s')>" % (self.id, self.ts, self.note[:50])
