import os
import yaml


class Configure(object):
    def __init__(self):
        self._cache = {}

    def from_dir(self, dir_name, force=False):
        cache_key = dir_name
        if not force:
            cached = self._cache.get(cache_key, None)
            if cached:
                return cached

        settings = {}
        for config_file in os.listdir(_abs(dir_name)):
            s = self.from_file(_abs(config_file, dir_name))
            if s:
                settings.update(s)

        self._cache[cache_key] = settings
        return settings

    def from_file(self, file_name):
        with open(file_name) as f:
            return yaml.load(f)

configure = Configure()


def _abs(name, prefix=None):
    if prefix:
        return os.path.abspath(os.path.join(prefix, name))
    return os.path.abspath(name)
