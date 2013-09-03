import logging
import bottle


log = logging.getLogger(__name__)

class Datastore(object):
    def init(self):
        pass

class DatastoreManager(object):
    def __getattr__(self, name):
        return self.__dict__[name]

    def register(self, name, ds):
        self.__dict__[name] = ds

    def init(self):
        for key in self.__dict__:
            ds = self.__dict__[key]
            ds.init()

datastores = DatastoreManager()

def setup_datastores(datastore_definitions):
    global datastores

    for definition in datastore_definitions:
        module = bottle.load(definition['ref'])
        ds = module.create_datastore(definition['config'])
        datastores.register(definition['name'], ds)

def init_datastores():
    datastores.init()