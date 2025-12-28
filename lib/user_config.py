from abc import ABC

import toml


class ConfigFile:
    # should reflect what's in config.toml

    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.config = toml.load(f)

    @property
    def refresh_interval(self):
        """The delay between each api call, in seconds."""
        return self.config['general']['refresh_interval']


# Make your class inheritate this one if it needs access to user configuration
class AppSettings(ABC):
    def __init__(self, config: ConfigFile):
        self.config = config
