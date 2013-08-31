import os
import yaml
from bottle import ConfigDict


class Configure(object):
    def from_dir(self, dir_name):
        settings = ConfigDict()
        for config_file in os.listdir(_abs(dir_name)):
            s = self.from_file(_abs(config_file, dir_name))
            if s:
                settings.load_dict(s)
        return settings

    def from_file(self, filename):
        with open(filename) as f:
            return yaml.load(f)

configure = Configure()


def _abs(name, prefix=None):
    if prefix:
        return os.path.abspath(os.path.join(prefix, name))
    return os.path.abspath(name)