import time

from lib.user_config import AppSettings, ConfigFile
from lib.display.display import Display
from lib.display.requestless_display import RequestlessDisplay
from lib.track import ColoredTrack, Track


class DisplayManager(Display, AppSettings):
    """Manages multiple displays to allow displaying the track information on multiple mediums from one API call."""
    displays: list[RequestlessDisplay] = []

    delay: int

    previousTrack: Track | None

    def __init__(self, api_key, config: ConfigFile):
        super().__init__(api_key)

        AppSettings.__init__(self, config)
        self.delay = self.config.refresh_interval
        self.previousTrack = Track.empty()

    def display(self):
        lastTrack = self.api.getLastTrack()
        nowPlayingStatus = self.api.isUserNowPlaying()

        if nowPlayingStatus:
            if self.previousTrack != lastTrack:
                self.previousTrack = lastTrack
                for display in self.displays:
                    display.show(
                        ColoredTrack.createFromTrack(
                            lastTrack,
                            self.getColorPalette(lastTrack.images[0].url),
                        )
                    )
        else:
            for display in self.displays:
                display.showNotPlaying()
