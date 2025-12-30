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

    @property
    def outputs(self) -> list[str]:
        """List of medium the color palette will be displayed to
            Possible values: ['terminal', 'LED'] """
        return self.__config['general']['outputs']

    @dataclass
    class Lastfm:
        api_key: str
        "Your Last.fm API key"
        username: str
        "Your Last.fm username"

    @property
    def lastfm(self):
        """ Configuration for Last.fm API, `None` if LASTFM isn't selected as the source."""
        return self.Lastfm(
            api_key=self.__config['LASTFM']['api_key'],
            username=self.__config['LASTFM']['username'],
        ) if self.source == 'LASTFM' else None

    @dataclass
    class Terminal:
        cover_dimensions: int
        "Size of the album cover displayed"

    @property
    def terminal(self):
        """ Configuration for Terminal display settings, `None` if Terminal isn't selected as a medium."""
        return self.Terminal(
            cover_dimensions=self.__config['terminal']['cover_dimension'],
        ) if "terminal" in self.outputs else None


# Make your class inheritate this one if it needs access to user configuration
class AppSettings(ABC):
    """
    Gives access to user configuration settings.
    """
    def __init__(self, config: ConfigFile):
        self.config = config
