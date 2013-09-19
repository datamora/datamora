import fudge
from bottling.factory import BottleSingletonAppLoader


class describe_load:
    
    @fudge.patch('bottle.load_app')
    def given_no_config_or_runtime_dependencies(self, bottle_load_app):
        app_ref = 'my_module:app'
        (bottle_load_app
            .expects_call()
            .with_args(app_ref)
            .returns({}))
        loader = BottleSingletonAppLoader(ref=app_ref)

        app = loader.load()

        assert app is not None
