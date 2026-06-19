import asyncio

from lib.api import LastFM, Params
from lib.display.dbus import Dbus
from lib.user_config import ConfigFile, Arguments
from lib.display.display_manager import DisplayManager
from lib.display.terminal import Terminal

import getopt, sys

async def main() -> None:
    # basic command line handling
    args = sys.argv[1:]
    options = "ho"
    long_options = ["help", "once"]

    argument = Arguments()

    try:
        argument = Arguments.createFromGetOpt(getopt.getopt(args, options, long_options))
    except getopt.error as err:
        print(str(err))

    configFile = ConfigFile("config.toml")

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
                displayManager.displays.append(Terminal(
                    source,
                    configFile
                ))
            case "dbus":
                displayManager.displays.append(Dbus())
                await displayManager.displays[-1].init()

            case _:
                raise RuntimeError(
                    f"Output '{output}' found in config file does not match any of the possible values ('terminal', 'LED')")

    if argument.once:
        displayManager.display()
    else:
        while True:
            displayManager.display()
            await asyncio.sleep(configFile.refresh_interval)

if __name__ == "__main__":
    asyncio.run(main())