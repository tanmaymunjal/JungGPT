import configparser
import os


class Config:
    _instance = None

    def __new__(cls, config_file="config.ini"):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = configparser.ConfigParser()
            cls._instance._load_config(config_file)
        return cls._instance

    def _load_config(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file {config_file} not found.")
        self._config.read(config_file)

    def get(self, section, option, fallback=None):
        return self._config.get(section, option, fallback=fallback)


config = Config()
