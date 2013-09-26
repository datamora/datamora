from bottling.wired import Container


class describe_Container:
    def it_initializes_with_a_spec(self):
        spec = {}
        c = Container(spec)

        assert c.spec == spec

class describe_Container_given_simple_spec_for_function_call:
    def it_returns_the_result_of_a_function_call_when_requested(self):
        spec = {
            'a_thing': 'thing_factory_function()'
        }
        c = Container(spec)

        thing = c.provide('a_thing')

        assert thing['name'] == 'Spkolorak'


def thing_factory_function():
    return {'name':'A thing!'}