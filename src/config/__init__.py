import os.path
from shutil import copyfile

import appdirs
import yaml


def get_property_from_dict(data: dict, name: str):
    if isinstance(data[name], dict):
        accessor = Accessor()
        accessor.data = data[name]
        return accessor
    return data[name]


class Config:
    APPLICATION_DIRECTORY = os.path.join(appdirs.user_config_dir(), 'openRGB_Ambientizer')
    CONFIG_FILE = os.path.join(APPLICATION_DIRECTORY, 'config.yml')
    if not os.path.isfile(CONFIG_FILE) or bool(os.getenv('USE_DEBUG_CONFIG')):
        os.makedirs(APPLICATION_DIRECTORY, exist_ok=True)
        copyfile(os.path.join(os.getcwd(), 'src', 'config', 'default.yml'), CONFIG_FILE)

    def __getattr__(self, item):
        with open(self.CONFIG_FILE, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return get_property_from_dict(data, item)
            except yaml.YAMLError as exc:
                print(exc)


class Accessor:
    data = {}

    def __getattr__(self, item):
        return get_property_from_dict(self.data, item)
