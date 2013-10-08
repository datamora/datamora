import sys


class Container(object):
    """Accepts a specification for wiring up components and provides methods for 
    materializing that spec as compnent instances"""

    def __init__(self, context, loader=None):
        """
        :param context: ``class:Context``
        :param loader: a callable that handles the actual loading/importing of components
        """
        self._context = context
        self._load = loader if loader else load
        self._components = {}
        self._factories = {}

    def get(self, ref):
        if self._components.has_key(ref):
            return self._components[ref]
        
        if self._factories.has_key(ref):
            component = self._factories[ref](self)
            self._components[ref] = component
            return component
        
        factory = self._context.get_factory(ref)
        self.add_reference(ref, factory)
        component = factory(self)
        self._components[ref] = component
        return component

    def add_reference(self, ref, factory):
        self._factories[ref] = factory

    def materialize(self, directive):
        definition = directive['create']
        source = definition['source']
        args = definition.get('args', {})
        return self.load(source, args)

    def resolve(self, ref):
        if not self._context.has_key(ref):
            raise UnknownDirectiveIdError()

        factory = self._context.get_factory(ref)
        return factory()

        directive = self._context[ref]
        definition = directive['create']
        source = definition['source']
        args = definition.get('args', {})
        return self.load(source, args)

    def load(self, source, args=None):
        if args is None:
            return self._load(source)
        return self._load(source, **args)


class Context(object):
    """Represents a context-scoped specification for wiring up components 
    and provides the relevant factories for materializing component instances
    for individual directives within the specification"""

    def __init__(self, spec):
        self._spec = spec

    def materialize(self, ref):
        directive = self._spec[ref]
        definition = directive['create']
        source = definition['source']
        args = definition.get('args', {})
        return self.load(source, args)

    def register(self, directive, factory):
        """Registers a handler that can  """

    def get_factory(self, ref):
        """Returns the relvant factory for the given directive id"""
        directive = self._spec[ref]



class SimpleCreateFactory(object):
    def create(self):
        return 



class UnknownDirectiveIdError(Exception):
    pass


def load(target, **namespace):
    """ Import a module or fetch an object from a module.

        * ``package.module`` returns `module` as a module object.
        * ``pack.mod:name`` returns the module variable `name` from `pack.mod`.
        * ``pack.mod:func()`` calls `pack.mod.func()` and returns the result.

        The last form accepts not only function calls, but any type of
        expression. Keyword arguments passed to this function are available as
        local variables. Example: ``import_string('re:compile(x)', x='[a-z]')``

        NOTE: Ripped straight from bottle.py!
    """
    module, target = target.split(":", 1) if ':' in target else (target, None)
    if module not in sys.modules: __import__(module)
    if not target: return sys.modules[module]
    if target.isalnum(): return getattr(sys.modules[module], target)
    package_name = module.split('.')[0]
    namespace[package_name] = sys.modules[package_name]
    return eval('%s.%s' % (module, target), namespace)


c4 = Container({
    'engine': {
        'create': {
            'source': 'sqlalchemy:create_engine(url, echo=echo)',
            'args': {
                'url': 'sqlite:///:memory:',
                'echo': False
            }
        }
    },
    'greeting': 'You have been "Hello"ed!',
    'greeter': {
        'create': {
            'source': 'bottling.wired:Greeter',
            'args': { 'greeting': { $ref:'greeting'} }
        }
    }
})
