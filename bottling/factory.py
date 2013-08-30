"""
bottle.ext.factory
====================

bottle-factory aims to provide some pattarns for building and using
pluggable apps to augment your own root apps.

:copyright: (c) 2011-2013 by FLC Ltd.
:license: BSD, see LICENSE.txt for more details.
"""

import os
import bottle


class MountAdapter:
    """Base adapter handling app mounts. It defines common/core
    functionality that may be overridden by more specific implementations.
    """
    def __init__(self, mount_def):
        self.ref = mount_def['ref']
        self.path = mount_def['path']
        self.config = mount_def.get('config')
        self.app = None
        self.meta = None

    def apply(self, target):
        target.mount(self.path, self.load_app())

    def load_app(self):
        return self.app

    def register_views(self):
        """Adds the given path to the list of bottle template paths"""
        if not self.meta.views_dir: return

        views_dir = self.meta.views_dir
        print 'dir ', views_dir
        if (os.path.exists(views_dir)):
            bottle.TEMPLATE_PATH.append(views_dir)
            print bottle.TEMPLATE_PATH


class PluggableMountAdapter(MountAdapter):
    """Adapter for pluggable app mount"""
    def load_app(self):
        if self.app:
            return self.app
        module = bottle.load(self.ref)
        self.app = module.create_app(self.config)
        self.meta = get_module_metadata(module)
        return self.app


class SingletonMountAdapter(MountAdapter):
    """Adapter for singleton app mount"""
    def load_app(self):
        if self.app:
            return self.app
        app = bottle.load_app(self.ref)
        if app and self.config:
            app.config.update(self.config)
        self.app = app
        return self.app


class MixinMountAdapter(MountAdapter):
    """Adapter for mixin app mount"""
    def apply(self, target):
        module = bottle.load(self.ref)
        module.create_app(self.config, target)

    def load_app(self):
        pass


class ModuleMetadata():
    def __init__(self, package_dir):
        self.views_dir = self._get_views_dir(package_dir)

    def _get_views_dir(self, package_dir):
        if package_dir:
            return os.path.abspath(os.path.join(package_dir, 'views'))
        return None


def extend(parent, mounts):
    """Given a list of mount definitions, it extends the parent app
    with each app depending on the type of mount point defined.
    """
    for mount_def in mounts:
        # get an appropriate mount adapter
        adapter = get_mount_adapter(mount_def)

        # apply the adapter to the parent app
        adapter.apply(parent)

        # register any views the referenced app may have
        adapter.register_views()


def get_mount_adapter(mount_def):
    """Returns an appropriate mount adapter for the given definition."""
    if mount_def.get('type') == 'singleton':
        return SingletonMountAdapter(mount_def)
    if mount_def.get('type') == 'mixin':
        return MixinMountAdapter(mount_def)
    return PluggableMountAdapter(mount_def)


def get_module_metadata(module):
    module_path = getattr(module, '__path__', [None])[0]
    return ModuleMetadata(module_path)

