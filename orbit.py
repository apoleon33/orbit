import time

from lib.api import LastFM, Params
from lib.user_config import ConfigFile, Arguments
from lib.display.display_manager import DisplayManager
from lib.display.view import Interface

import getopt, sys

if __name__ == "__main__":
    # basic command line handling
    args = sys.argv[1:]
    options = "ho"
    long_options = ["help", "once"]

    argument = Arguments()

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-h", "--help"):
                print("TODO: do help part")
            elif currentArg in ("-o", "--once"):
                argument.once = True
    except getopt.error as err:
        print(str(err))

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

    if argument.once:
        displayManager.display()
    else:
        while True:
            displayManager.display()
            time.sleep(configFile.refresh_interval)
