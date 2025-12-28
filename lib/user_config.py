from abc import ABC
from dataclasses import dataclass

import toml


class ConfigFile:
    # should reflect what's in config.toml

    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.__config = toml.load(f)

    @property
    def refresh_interval(self):
        """The delay between each api call, in seconds."""
        return self.__config['general']['refresh_interval']

    @property
    def source(self):
        """The API to use to query the music from.
            Possible values: ['LASTFM']"""
        return self.__config['general']['source']

    @dataclass
    class Lastfm:
        api_key: str
        username: str

    @property
    def lastfm(self):
        """ Configuration for Last.fm API, `None` if LASTFM isn't selected as the source."""
        return self.Lastfm(
            api_key=self.__config['LASTFM']['api_key'],
            username=self.__config['LASTFM']['username'],
        ) if self.source == 'LASTFM' else None


# Make your class inheritate this one if it needs access to user configuration
class AppSettings(ABC):
    def __init__(self, config: ConfigFile):
        self.config = config
