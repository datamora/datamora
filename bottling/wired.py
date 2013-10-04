import sys


class Context(object):
    """Accepts a specification for wiring up components and provides methods for 
    materializing that spec as compnent instances"""

    def __init__(self, spec, loader=None):
        """
        :param wire_spec: `dict`
        :param loader: a callable that handles the actual loading/importing of components
        """
        self._spec = spec
        self._load = loader if loader else load
        self._components = {}

    def register(self, ref, component):
        self._components[ref] = component
        return component

    def get(self, ref):
        if self._components.has_key(ref):
            return self._components[ref]
        return self.register(ref, self.resolve(ref))

    def resolve(self, ref):
        if not self._spec.has_key(ref):
            raise UnknownDirectiveIdError()

        factory = self._spec.get_factory(ref)
        return factory.create()

        directive = self._spec[ref]
        definition = directive['create']
        source = definition['source']
        args = definition.get('args', {})
        return self.load(source, args)

    def load(self, source, args=None):
        if args is None:
            return self._load(source)
        return self._load(source, **args)


class Specification(object):
    """Represents a context-scoped specification for wiring up components 
    and provides the relevant factories for materializing component instances
    for individual directives within the specification"""

    def __init__(self, data):
        self._data = data

    def get_factory(self, ref):
        """Returns the relvant factory for the given directive id"""
        directive = self._data[ref]


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
    hello: 'You have been "Hello"ed!',
    engine: {
        'create': {
            'source': 'sqlalchemy:create_engine(url, echo=echo)',
            'args': {
                'url': 'sqlite:///:memory:',
                'echo': False
            }
        }
    },

})
