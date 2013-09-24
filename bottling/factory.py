"""
bottle.ext.factory
====================

bottling-factory aims to explore and promote some patterns for 
composing complex applications by mixing and matching simple pluggable apps.

:copyright: (c) 2011-2013 by FLC Ltd.
:license: BSD, see LICENSE.txt for more details.
"""

import os
import logging
import bottle


# =========================================================
# Parts and Builder
# =========================================================

class Builder(object):
    """Converts a stack of mount definitions into a stack of apps"""

    def __init__(self, app_loaders, logger=None):
        self._loaders = app_loaders
        self._logger = logger or logging.getLogger(__name__)
        
    def build(self, composition_parts, dependency_resolver):
        root = bottle.Bottle()
        mount_defs = composition_parts['mounts']
        for mount_def in mount_defs:
            part = MountablePart(mount_def['ref'], mount_def)

            self._logger.info('Mounting %s at %s' % (part.ref, part.path))

            app = self.get_app_for_part(part, dependency_resolver)
            root.mount(part.path, app)
        return root

    def get_app_for_part(self, part, dependency_resolver):
        deps = dependency_resolver.resolve(part.deps)
        app_loader = self._loaders[part.kind]

        return app_loader(part.ref, part.config, deps)


class MountablePart(object):
    """A mountable part based on a mount definition."""

    def __init__(self, ref, options):
        self.ref = options['ref']
        self.path = options.get('path', '/')
        self.config = options.get('config')
        self.deps = options.get('deps')
        self._kind = options.get('kind')

    @property
    def kind(self):
        if not self._kind:
            self._kind = self._guess_kind()

        return self._kind
    
    def _guess_kind(self):
        is_singleton = ':' in self.ref
        return Kind.SINGLETON if is_singleton else Kind.PLUGGABLE


class Kind(object):
    SINGLETON = 'singleton'
    PLUGGABLE = 'pluggable'




# =========================================================
# Loaders and Resolvers
# =========================================================

def load_pluggable_app(ref, config=None, deps=None):
    module = bottle.load(ref)

    meta = get_module_metadata(module)
    if meta.views_dir:
        register_views_dir(meta.views_dir)

    return module.create_app(config=config, **deps)


def load_singleton_app(ref, config=None, deps=None):
    if ':' in ref:
        module = bottle.load(ref.split(':')[0])
    else:
        module = bottle.load(ref)

    meta = get_module_metadata(module)
    if meta.views_dir:
        register_views_dir(meta.views_dir)

    app = bottle.load_app(ref)
    if app and config:
        app.config.update(config)
    return app


class ConfigBasedResolver(object):
    """Resolvs dependencies by mapping references to config based instances"""
    def __init__(self, **kwargs):
        self._logger = kwargs.get('logger') or logging.getLogger(__name__)
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def resolve(self, dependencies):
        instances = {}
        if not dependencies:
            return instances

        for handle in dependencies:
            dep = dependencies[handle]
            if dep.startswith('$'):
                area = dep[1:].split(':')[0]
                key = dep[1:].split(':')[1]
                pointers = getattr(self, area)
                instance = getattr(pointers, key)
                instances[handle] = instance

        return instances



# =========================================================
# App module metadata
# =========================================================

class ModuleMetadata():
    def __init__(self, package_dir):
        self.views_dir = self._get_views_dir(package_dir) if package_dir else None

    def _get_views_dir(self, package_dir):
        views_dir = os.path.abspath(os.path.join(package_dir, 'views'))
        if os.path.exists(views_dir):
            return views_dir

        templates_dir = os.path.abspath(os.path.join(package_dir, 'templates'))
        if os.path.exists(templates_dir):
            return templates_dir

        return None


def get_module_metadata(module):
    module_path = getattr(module, '__path__', [None])[0]
    return ModuleMetadata(module_path)

def register_views_dir(views_dir):
    """Adds the given path to the list of bottle template paths"""
    if not views_dir:
        return

    if os.path.exists(views_dir) and views_dir not in bottle.TEMPLATE_PATH:
        bottle.TEMPLATE_PATH.append(views_dir)




# =========================================================
# Default helpers
# =========================================================

app_loaders = {Kind.SINGLETON:load_singleton_app, Kind.PLUGGABLE:load_pluggable_app}
builder = Builder(app_loaders)
