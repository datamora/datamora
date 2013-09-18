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
        fake_app = fudge.Fake('app').is_a_stub()
        fake_loader = (fudge.Fake('loader')
                            .expects('load')
                            .with_args(a_mount.ref)
                            .returns(fake_app))
        def fake_resolver():
            pass
        
        adapter = MountAdapter(a_mount, fake_loader, fake_resolver)
        app = adapter.load_app()

        assert app is not None

    @fudge.test
    def it_returns_a_cached_app_if_it_is_already_loaded(self):
        a_mount = Mount(dict(path='/', ref='dummy_app'))
        fake_app = fudge.Fake('app').is_a_stub()
        fake_loader = (fudge.Fake('loader')
                            .expects('load')
                            .with_args(a_mount.ref)
                            .times_called(1)
                            .returns(fake_app))
        def fake_resolver():
            pass

        adapter = MountAdapter(a_mount, fake_loader, fake_resolver)
        app1 = adapter.load_app()
        app2 = adapter.load_app()

        assert app1 == app2


# class describe_apply:

#     def it_mounts_the_referenced_app_on_the_target_at_the_given_path(self):

#         adapter = MountAdapter(a_mount, fake_loader, fake_resolver)

#         adapter.mount(target_app, path)
