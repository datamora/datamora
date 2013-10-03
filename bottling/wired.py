import sys


class Container(object):
    """Accepts a specification for wiring up components and materializes that spec 
    as a context"""
    def __init__(self, spec, loader=None):
        self._spec = spec
        self._load = loader if loader else load
        self._context = {}

    def register(self, handle, component):
        self._context[handle] = component
        return component

    def get(self, handle):
        if self._context.has_key(handle):
            return self._context[handle]
        return self.register(handle, self.resolve(handle))

    def resolve(self, handle):
        if not self._spec.has_key(handle):
            raise UnknownHandleError()

        definition = self._spec[handle]['create']
        source = definition['source']
        args = definition.get('args', {})
        return self.load(source, args)

    def load(self, source, args=None):
        if args is None:
            return self._load(source)
        return self._load(source, **args)


        


class UnknownHandleError(Exception):
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


# wire({
#     'datastores.master.engine': {
#         'create': {
#             'from': 'sqlalchemy:create_engine(url, echo=echo)',
#             'args': {
#                 'url': 'sqlite:///:memory:',
#                 'echo': False
#             }
#         }
#     }
# })
