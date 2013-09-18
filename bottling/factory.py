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


# =========================================================
# Mount Definition and Adapter
# =========================================================

class Mount(object):
    """A mount object. Describes a mount point based on provided 
    mount point definition."""

    def __init__(self, mount_def):
        self.path = mount_def['path']
        self.ref = mount_def['ref']
        self.kind = mount_def.get('kind')
        self.config = mount_def.get('config')
        self.inject = mount_def.get('inject')
        

class MountAdapter(object):
    """Base adapter handling app mounts. It defines common/core
    functionality that may be overridden by more specific implementations.

    Example mount def::

        path: /hello
        ref: apps.greeter
        config:
            style: serious
        inject:
            datastore: $master
    """

    def __init__(self, mount, app_loader, deps_resolver):
        self._mount = mount
        self._loader = app_loader
        self._resolver = deps_resolver
        self._app = None
        self._meta = None

    def apply(self, target):
        target.mount(self.path, self.load_app())

    def load_app(self):
        # if self._app:
        #     return self._app
        app = self._loader.load(self._mount.ref)

        # self.meta = self.get_module_metadata(module)
        # return self._app
        return app

    def register_views(self):
        """Adds the given path to the list of bottle template paths"""
        if not self._meta.views_dir:
            return

        views_dir = self._meta.views_dir
        if (os.path.exists(views_dir)):
            bottle.TEMPLATE_PATH.append(views_dir)


class MergeMountAdapter(MountAdapter):
    pass
        



# =========================================================
# App loaders
# =========================================================

class BottlePluggableAppLoader(object):
    """Uses `bottle.load` to load bottle-based wsgi apps"""
    def __init__(self, ref, kind=None, config=None):
        self.ref = ref
        self.kind = kind

    def load(self):
        module = bottle.load(self.ref)
        return module.create_app()


class BottleSingletonAppLoader(object):
    """Uses `bottle.load_app` to load bottle-based wsgi apps"""
    def __init__(self, ref, kind=None, config=None):
        self.ref = ref
        self.kind = kind

    def load(self):
        app = bottle.load_app(self.ref)
        return app
        



class PluggableMountAdapter(MountAdapter):
    """Adapter for pluggable app mount"""
    def load_app(self, config=None, deps=None):
        if self.app:
            return self.app
        module = bottle.load(self.ref)
        try:
            self.app = module.app
        except AttributeError:
            pass
        self.app = module.create_app(self.config, **self.resolve(deps))
        self.meta = get_module_metadata(module)
        return self.app


class SingletonMountAdapter(MountAdapter):
    """Adapter for singleton app mount"""
    def load_app(self, config=None):
        if self.app:
            return self.app
        app = bottle.load_app(self.ref)
        if app and config:
            app.config.update(config)
        self.app = app
        return self.app


class MixinMountAdapter(MountAdapter):
    """Adapter for mixin app mount"""
    def apply(self, target, config=None):
        module = bottle.load(self.ref)
        module.create_app(self.instance_config, target)

    def load_app(self):
        pass


class MergeMountAdapter(PluggableMountAdapter):
    """Adapter for merge app mount"""
    def apply(self, target):
        target.merge(self.load_app())


class ModuleMetadata():
    def __init__(self, package_dir):
        self.views_dir = self._get_views_dir(package_dir)

    def _get_views_dir(self, package_dir):
        if package_dir:
            return os.path.abspath(os.path.join(package_dir, 'views'))
        return None




class AdapterRegistry(object):
    def register(self, adapter):
        pass


def mount_all(parent, mount_defs, app_loader, deps_resolver):
    """Given a list of mount definitions, it extends the parent app
    with each app depending on the type of mount point defined.
    """
    for mount_def in mount_defs:
        mount(parent, mount_def, resolver)


def mount(parent, mount_def, app_loader, deps_resolver):
    # get an appropriate mount adapter
    adapter = get_mount_adapter(mount_def, app_loader, deps_resolver)

    # apply the adapter to the parent app
    adapter.apply(parent)

    # register any views the referenced app may have
    adapter.register_views()


def get_mount_adapter(mount_def, settings):
    """Returns an appropriate mount adapter for the given definition."""
    if mount_def.get('type') == 'singleton':
        return SingletonMountAdapter(mount_def, settings)
    if mount_def.get('type') == 'mixin':
        return MixinMountAdapter(mount_def, settings)
    if mount_def.get('type') == 'merge':
        return MergeMountAdapter(mount_def, settings)
    return PluggableMountAdapter(mount_def, settings)


def get_module_metadata(module):
    module_path = getattr(module, '__path__', [None])[0]
    return ModuleMetadata(module_path)
