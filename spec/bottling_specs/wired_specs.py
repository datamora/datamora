import fudge
from bottling.wired import Container, Loader


class describe_Container:

    def it_initializes_with_a_spec(self):
        spec = {}
        c = Container(spec)

        assert c.spec == spec


class describe_Container_given_simple_spec_for_function_call:

    def _returns_the_result_of_a_function_call_when_requested(self):
        spec = {
            'a_thing': 'thing_factory_function()'
        }
        c = Container(spec)

        thing = c.provide('a_thing')

        assert thing['name'] == 'Spkolorak'



class describe_load:

    @fudge.patch('bottle.load')
    def it_loads_a_module_by_reference(self, bottle_load):
        module_ref = 'my_module'
        loaded_module = fudge.Fake('module')
        (bottle_load
            .expects_call()
            .with_args(module_ref)
            .returns(loaded_module))

        #m = load(module_ref)

        assert m is not None

    @fudge.patch('bottle.load')
    def it_loads_a_variable_from_a_module(self, bottle_load):
        var_ref = 'my_module:a_var'
        loaded_module = fudge.Fake('module').provides('a_var')
        (bottle_load
            .expects_call()
            .with_args(var_ref)
            .returns(loaded_module))

        v = load(var_ref)

        assert v is not None


def thing_factory_function():
    return {'name':'A thing!'}
