
class Container(object):
    """Holds the context for a wire spec"""
    def __init__(self, spec):
        self.spec = spec

    def _is_simple_spec(self, spec):
        return type(spec) is str

    def provide(self, handle):
        the_spec = self.spec[handle]
        if self._is_simple_spec(the_spec):
            return eval(the_spec)
