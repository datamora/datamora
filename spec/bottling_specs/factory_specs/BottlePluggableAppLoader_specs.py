import fudge
from bottling.factory import BottlePluggableAppLoader


class describe_load:
    
    @fudge.patch('bottle.load')
    def given_no_config_or_dependencies_it_loads_an_app_by_reference(self, bottle_load):
        app_ref = 'my_module'
        loaded_module = fudge.Fake('module').provides('create_app').returns({})
        (bottle_load
            .expects_call()
            .with_args(app_ref)
            .returns(loaded_module))
        loader = BottlePluggableAppLoader(ref=app_ref)

        app = loader.load()

        assert app is not None

    def it_captures_metadata_for_app(self):
        app_ref = 'my_module'

        loader = BottlePluggableAppLoader(ref=app_ref)
