import fudge
from bottling.factory import BaseBottleAppLoader


class describe_init:

    def it_initializes_with_given_options(self):
        ref = 'my_module'
        kind = None
        
        loader = BaseBottleAppLoader(ref, kind)

        assert loader.ref == ref
        assert loader.kind == None
