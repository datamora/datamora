from bottling.factory import Mount


class describe_init:

    def it_initializes_with_given_mount_definition(self):
        mount_def = dict(
            path = '/mount-point',
            ref = 'reference.to.my:app',
            config = {'option':True}
        )

        mount = Mount(mount_def)

        assert mount.path == mount_def['path']
        assert mount.ref == mount_def['ref']
        assert mount.config == mount_def['config']

    def it_provides_defaults_for_missing_options(self):
        mount_def = dict(
            path = '/mount-point',
            ref = 'reference.to.my:app'
        )

        mount = Mount(mount_def)

        assert mount.kind == None
        assert mount.config == None
        assert mount.inject == None
