from lib.api import LastFM, Params
from lib.user_config import ConfigFile
from lib.display.display_manager import DisplayManager
from lib.display.view import Interface

if __name__ == "__main__":
    configFile = ConfigFile("config_example.toml")

    match configFile.source:
        case "LASTFM":
            source = LastFM(
                Params(configFile),
            )
        case _:
            raise RuntimeError(
                f"Source '{configFile.source}' found in config file does not match any of the possible values ('LASTFM')")

    displayManager = DisplayManager(
        source,
        configFile
    )

    for output in configFile.outputs:
        match output:
            case "terminal":
                displayManager.displays.append(Interface(
                    source,
                    configFile
                ))
            case _:
                raise RuntimeError(
                    f"Output '{output}' found in config file does not match any of the possible values ('terminal', 'LED')")

    while True:
        displayManager.display()
