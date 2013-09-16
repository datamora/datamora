from bottling.factory import Mount, MountAdapter


class describe_init:
    
    def it_initializes_with_given_options(self):
        fake_mount = Mount(dict(path='/', ref='dummy_app'))
        def fake_loader():
            pass
        def fake_resolver():
            pass

        adapter = MountAdapter(fake_mount, fake_loader, fake_resolver)

        assert adapter.mount == fake_mount
        assert adapter.loader == fake_loader
        assert adapter.resolver == fake_resolver
