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

    def apply(self, target):
        target.mount(self.path, self.load_app())

    def register_views(self):
        register_app_views(self.load_app())

    def load_app(self):
        return self.app


class PluggableMountAdapter(MountAdapter):
    """Adapter for pluggable app mount"""
    def load_app(self):
        if self.app:
            return self.app
        module = bottle.load(self.ref)
        self.app = module.create_app(self.config)
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


def register_app_views(app):
    """Checks to see if the app has a `root_path` property.
    If yes, then it registers the path to the app views dir
    """
    root_path = _get_app_root_path(app)
    if root_path:
        views_dir = os.path.abspath(os.path.join(root_path, 'views'))
        print views_dir
        register_views_dir(views_dir)


def register_views_dir(path):
    """Adds the given path to the list of bottle template paths"""
    if (os.path.exists(path)):
        bottle.TEMPLATE_PATH.append(path)


def _get_app_root_path(app):
    try:
        return app.__path__
    except:
        return None
