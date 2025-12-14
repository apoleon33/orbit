# python
import os

import climage
import requests

from lib.display.display import Display
from lib.display.requestless_display import RequestlessDisplay

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


class Interface(Display, RequestlessDisplay):
    padding = "     "
    def __init__(self, api):
        super().__init__(api)
        self.now_playing_line_number = 8
        self.not_playing_line_number = 1
        self.left_padding = "   "
        self.cover_dimensions = 20
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

        imageArt = climage.convert('temp.jpg', width=40).split("[0m")

        output = f"{imageArt[0]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Music detected!', Ansi.BOLD, Ansi.RED)}"
        output += f"{imageArt[1]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Name: ', Ansi.BOLD, Ansi.RED)}{track.name}"
        output += f"{imageArt[2]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Artist: ', Ansi.BOLD, Ansi.RED)}{track.artist.name}"
        output += f"{imageArt[3]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('Album: ', Ansi.BOLD, Ansi.RED)}{track.album.name}"
        output += f"{imageArt[4]}{Ansi.DEFAULT}{self.padding}{self.delimiter}"
        output += f"{imageArt[5]}{Ansi.DEFAULT}{self.padding}{Ansi.formatText('LastFM Username: ', Ansi.BOLD, Ansi.RED)}{self.api.username}"

        for line in imageArt[6:]:
            output += f"{line}"

        output += Ansi.DEFAULT

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
