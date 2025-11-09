# python
import os

from lib.display.display import Display
from lib.display.requestless_display import RequestlessDisplay


class Interface(Display, RequestlessDisplay):
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
        output = "Music detected!\n"

        output += f"Name: {track.name}\n"
        output += f"Artist: {track.artist.name}\n"
        output += f"Album: {track.album.name}\n"
        output += f"{self.delimiter}\n"
        output += f"LastFM Username: {self.api.username}\n"

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
