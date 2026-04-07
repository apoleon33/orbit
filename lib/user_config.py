from abc import ABC
from dataclasses import dataclass

import toml
from click import argument


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
        "Your Last.fm API key."
        username: str
        "Your Last.fm username."
        extended_info: bool
        "Wether to display the lastfm username and the scrobble count in the Terminal"

    @property
    def lastfm(self):
        """ Configuration for Last.fm API, `None` if LASTFM isn't selected as the source."""
        return self.Lastfm(
            api_key=self.__config['LASTFM']['api_key'],
            username=self.__config['LASTFM']['username'],
            extended_info=self.__config['LASTFM']['extended_info'],
        ) if self.source == 'LASTFM' else None

    @dataclass
    class Terminal:
        cover_dimensions: int
        "Size of the album cover displayed"

        _color_depth: str

        @property
        def color_depth(self) -> str:
            """Color depth of the album cover, possible values: ['true_color', '256', '16', '8']"""
            assert self._color_depth in ['true_color', '256', '16', '8'], f"Color depth not one of the possible values, got {self._color_depth}, expected 'true_color', '256', '16', '8'"
            return self._color_depth

    @property
    def terminal(self):
        """ Configuration for Terminal display settings, `None` if Terminal isn't selected as a medium."""
        return self.Terminal(
            cover_dimensions=self.__config['terminal']['cover_dimension'],
            _color_depth=self.__config['terminal']['color_depth']
        ) if "terminal" in self.outputs else None




# Make your class inheritate this one if it needs access to user configuration
class AppSettings(ABC):
    """
    Gives access to user configuration settings.
    """
    def __init__(self, config: ConfigFile):
        self.config = config

class Arguments:
    """
    Class handling command line arguments.
    """

    once: bool
    """If set to true, the program will run only once and then exit."""
    def __init__(self, once: bool=False):
        self.once = once

    @staticmethod
    def createFromGetOpt(output: tuple) -> Arguments:
        """create an Arguments object from those acquired via getopt"""
        argument = Arguments()
        arguments, value = output
        for currentArg, currentVal in arguments:
            if currentArg in ("-h", "--help"):
                print("TODO: do help part")
            elif currentArg in ("-o", "--once"):
                argument.once = True

        return argument