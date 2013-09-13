from compare import expect
from bottling.factory import Mount, BottlePluggableAppLoader, MountAdapter


class DescribeMount(object):
    def it_initializes_with_given_mount_def(self):
        mount_def = dict(
            path = '/mount-point',
            ref = 'reference.to.my:app',
            config = {'option':True}
        )

        mount = Mount(mount_def)

        expect(mount.path).to_be(mount_def['path'])
        expect(mount.ref).to_be(mount_def['ref'])
        expect(mount.config).to_equal(mount_def['config'])

    def it_provides_defaults_for_missing_options(self):
        mount_def = dict(
            path = '/mount-point',
            ref = 'reference.to.my:app'
        )

        mount = Mount(mount_def)

        expect(mount.kind).to_equal(None)
        expect(mount.config).to_equal(None)
        expect(mount.inject).to_equal(None)


class DescribeBottlePluggableAppLoader(object):
    def it_initializes_with_given_options(self):
        ref = 'my.app:app'
        kind = None
        
        loader = BottlePluggableAppLoader(ref, kind)

        expect(loader.ref).to_equal(ref)
        expect(loader.kind).to_be(None)

class DescribeBottlePluggableAppLoader_load(object):
    def it_loads_the_app_given_no_instance_config_and_runtime_dependencies(self):
        loader = BottlePluggableAppLoader(ref='my:app')

        app = loader.load()

        expect(app).NOT.to_be(None)
        

class DescribeMountAdapter(object):
    def it_initializes_with_given_options(self):
        fake_mount = Mount(dict(path='/', ref='dummy_app'))
        def fake_loader():
            pass
        def fake_resolver():
            pass

        adapter = MountAdapter(fake_mount, fake_loader, fake_resolver)

        expect(adapter.mount).to_be(fake_mount)
        expect(adapter.loader).to_be(fake_loader)
        expect(adapter.resolver).to_be(fake_resolver)
