import os
import yaml


# global settings
settings = {}


class ConfigLoader(object):
    def __init__(self):
        self._cache = {}

    def from_dir(self, dir_name, force=False):
        cache_key = dir_name
        if not force:
            cached = self._cache.get(cache_key, None)
            if cached:
                return cached

        values = {}
        for config_file in os.listdir(_abs(dir_name)):
            s = self.from_file(_abs(config_file, dir_name))
            if s:
                values.update(s)

        self._cache[cache_key] = values
        return values

    def from_file(self, file_name):
        with open(file_name) as f:
            return yaml.load(f)


"""Default instance of :class:`ConfigLoader` used by `configure`"""
default_loader = ConfigLoader()

def load_settings(config_dir, force=False):
    """Loads the configuration from the `config_dir` into the global `settings`"""
    global settings
    settings = default_loader.from_dir(config_dir, force)


def _abs(name, prefix=None):
    if prefix:
        return os.path.abspath(os.path.join(prefix, name))
    return os.path.abspath(name)
