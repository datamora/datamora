import fudge
from bottling.factory import Mount, MountAdapter


class describe_init:
    
    def it_initializes_with_given_options(self):
        a_mount = Mount(dict(path='/', ref='dummy_app'))
        def fake_loader():
            pass
        def fake_resolver():
            pass

        adapter = MountAdapter(a_mount, fake_loader, fake_resolver)

        assert adapter._mount == a_mount
        assert adapter._loader == fake_loader
        assert adapter._resolver == fake_resolver


class describe_load_app:

    @fudge.test
    def it_uses_the_app_loader_to_fetch_the_app_by_reference(self):
        a_mount = Mount(dict(path='/', ref='dummy_app'))
        fake_loader = (fudge.Fake('loader')
                            .expects('load')
                            .with_args(a_mount.ref)
                            .returns({}))
        def fake_resolver():
            pass
        
        adapter = MountAdapter(a_mount, fake_loader, fake_resolver)
        app = adapter.load_app()

        assert app is not None
