import fudge
from bottling.factory import BottlePluggableAppLoader


class describe_init:

    def it_initializes_with_given_options(self):
        ref = 'my.app:app'
        kind = None
        
        loader = BottlePluggableAppLoader(ref, kind)

        assert loader.ref == ref
        assert loader.kind == None


class describe_load:
    
    @fudge.patch('bottle.load')
    def given_no_config_and_runtime_dependencies(self, bottle_load):
        app_ref = 'my:app'
        loaded_module = fudge.Fake('module').provides('create_app').returns({})
        (bottle_load
            .expects_call()
            .with_args(app_ref)
            .returns(loaded_module))
        loader = BottlePluggableAppLoader(ref=app_ref)

        app = loader.load()

        assert app is not None
