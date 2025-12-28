import os

from dotenv import load_dotenv

from lib.api import LastFM, Params
from lib.user_config import ConfigFile
from lib.display.display_manager import DisplayManager
from lib.display.view import Interface

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    assert api_key is not None, "No LastFM api key found"

    configFile = ConfigFile("config_example.toml")

    displayManager = DisplayManager(
        LastFM(
            Params(apiKey=api_key, user="apoleon33"),
        ),
        configFile
    )

    displayManager.displays.append(Interface(
        LastFM(
            Params(apiKey=api_key, user="apoleon33"),
        )
    ))

    while True:
        displayManager.display()
