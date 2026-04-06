# python
import math
import os
from operator import indexOf

import climage
import requests
from Pylette import Color, Palette

from lib.display.display import Display
from lib.display.requestless_display import RequestlessDisplay
from lib.user_config import AppSettings, ConfigFile


class Ansi:
    DEFAULT = "[0m"
    BLACK = "30m"
    RED = "[31m"
    GREEN = "[32m"
    YELLOW = "[33m"
    BLUE = "[34m"
    MAGENTA = "[35m"
    CYAN = "[36m"
    WHITE = "[37m"
    BRIGHT_BLACK = "[90m"
    BRIGHT_RED = "[91m"
    BRIGHT_GREEN = "[92m"
    BRIGHT_YELLOW = "[93m"
    BRIGHT_BLUE = "[94m"
    BRIGHT_MAGENTA = "[95m"
    BRIGHT_CYAN = "[96m"
    BRIGHT_WHITE = "[97m"

    DEFAULT_FORMATTING = "[22m"
    BOLD = "[1m"
    UNDERLINE = "[4m"
    REVERSED = "[7m"
    POSITIVE = "[27m"

    @staticmethod
    def formatText(content, *args):
        return f"{''.join(args)}{content}{Ansi.DEFAULT}"

    @staticmethod
    def applyColor(color: tuple):
        assert len(color) == 3
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


class Terminal(Display, RequestlessDisplay, AppSettings):
    """Display the album cover as well as the tracks information in the terminal."""
    padding = "     "

    _rowIndex: int = 0  # is used to keep track when lining up everything

    def __init__(self, api, configFile: ConfigFile):
        super().__init__(api)
        AppSettings.__init__(self, configFile)
        self.now_playing_line_number = 8
        self.not_playing_line_number = 1
        self.left_padding = "   "
        self.cover_dimensions = self.config.terminal.cover_dimensions
        self.delimiter = "------------------------"

    def _clearTerminal(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def format_output(self, track) -> str:
        img = requests.get(track.images[0].url).content
        tempFile = open("temp.jpg", "wb")

        tempFile.write(img)
        tempFile.close()

        imageArt = climage.convert('temp.jpg',
                                   is_truecolor=self.config.terminal.color_depth == "true_color",
                                   is_256color=self.config.terminal.color_depth == "256",
                                   is_16color=self.config.terminal.color_depth == "16",
                                   is_8color=self.config.terminal.color_depth == "8",
                                   width=self.cover_dimensions
                                   ).split("[0m")

        colorPalette = self.getColorPalette(track.images[0].url)

        # compute the best color to display text
        colorRatios = [self.getContrast(color) for color in colorPalette.colors]
        primaryColor = colorPalette.colors[indexOf(colorRatios, min(colorRatios))]

        if min(colorRatios) > 1 / 2:
            # print(f"no ideal contrast found, defaulting to pure white, got {min(colorRatios)}")
            primaryColor = Color((255, 255, 255, 1), 100)

        output = f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Music detected!', Ansi.BOLD, Ansi.applyColor(primaryColor.rgb))}"
        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Name: ', Ansi.BOLD, Ansi.applyColor(primaryColor.rgb))}{track.name}"
        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Artist: ', Ansi.BOLD, Ansi.applyColor(primaryColor.rgb))}{track.artist.name}"
        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Album: ', Ansi.BOLD, Ansi.applyColor(primaryColor.rgb))}{track.album.name}"
        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}{self.delimiter}"

        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}"
        if self.config.source == "LASTFM":
            output += f"{Ansi.formatText('LastFM Username: ', Ansi.BOLD, Ansi.applyColor(primaryColor.rgb))}{self.api.username}"
            output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('total scrobbles: ', Ansi.BOLD, Ansi.applyColor(primaryColor.rgb))}{self.api.totalScrobbles}"

        # display the color palette blocks (2 "for" for 2 lines)
        output += f"{imageArt[self.index]}"
        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}"
        for color in colorPalette.colors[0:6]:
            output += f"{Ansi.applyColor(color.rgb)}███"

        output += f"{imageArt[self.index]}{Ansi.DEFAULT}{self.padding}"
        for color in colorPalette.colors[6:]:
            output += f"{Ansi.applyColor(color.rgb)}███"

        for line in imageArt[self.index:]:
            output += f"{line}{Ansi.DEFAULT}"

        output += Ansi.DEFAULT

        # reset the index
        self._rowIndex = 0

        return output

    def display(self):
        last_track = self.api.getLastTrack()
        now_playing_status = self.api.isUserNowPlaying()
        if now_playing_status:
            self._clearTerminal()
            print(self.format_output(last_track))
            print(self.delimiter)
            print()
        else:
            self._clearTerminal()
            print("no music currently playing, retrying in 15s...")

    def show(self, track):
        self._clearTerminal()
        print(self.format_output(track))

    def showNotPlaying(self):
        self._clearTerminal()
        print("No music currently playing!")

    def getContrast(self, color: Color) -> float:
        """Return the color contrast compared to the background assuming the background is pure black."""

        # s/o https://dev.to/alvaromontoro/building-your-own-color-contrast-checker-4j7o
        # luminance
        def computeColorParts(value: int):
            value /= 255
            return value / 12.92 if value <= 0.03928 else math.pow((value + 0.055) / 1.055, 2.4)

        colorLuminance = 0.2126 * computeColorParts(color.rgb[0]) + 0.7152 * computeColorParts(
            color.rgb[1]) + 0.0722 * computeColorParts(color.rgb[2])

        ratio = (0.05 / (colorLuminance + 0.05))

        # let's assume a terminal display is a small text
        return ratio

    @property
    def index(self) -> int:
        assert self._rowIndex <= self.cover_dimensions
        self._rowIndex += 1
        return self._rowIndex - 1