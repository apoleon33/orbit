from lib.api import LastFM, Params
from lib.user_config import ConfigFile
from lib.display.display_manager import DisplayManager
from lib.display.view import Interface

if __name__ == "__main__":
    configFile = ConfigFile("config_example.toml")

    displayManager = DisplayManager(
        LastFM(
            Params(configFile),
        ),
        configFile
    )

    displayManager.displays.append(Interface(
        LastFM(
            Params(configFile),
        )
    ))

    while True:
        displayManager.display()
