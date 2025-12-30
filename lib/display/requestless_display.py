from abc import ABC

from lib.track import ColoredTrack


class RequestlessDisplay(ABC):
    """Display that does not require making the API calls itself, but rather get infos passed via arguments"""
    def show(self, track: ColoredTrack): pass

    def showNotPlaying(self): pass