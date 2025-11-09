import time

from lib.display.display import Display
from lib.display.requestless_display import RequestlessDisplay
from lib.track import ColoredTrack


class DisplayManager(Display):
    displays: list[RequestlessDisplay] = []

    delay: int

    def __init__(self, api_key, delay=15):
        super().__init__(api_key)
        self.delay = delay

    def display(self):
        lastTrack = self.api.getLastTrack()
        nowPlayingStatus = self.api.isUserNowPlaying()

        if nowPlayingStatus:
            for display in self.displays:
                display.show(
                    ColoredTrack.createFromTrack(
                        lastTrack,
                        self.getColorPalette(lastTrack.images[0].url),
                    )
                )

        time.sleep(self.delay)
