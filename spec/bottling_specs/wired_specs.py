from bottling.wired import Container


class describe_Container:
    def it_initializes_with_a_spec(self):
        spec = {}
        c = Container(spec)

        assert c.spec == spec