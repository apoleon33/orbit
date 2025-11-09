from abc import ABC

from lib.track import ColoredTrack


class RequestlessDisplay(ABC):
    def show(self, track: ColoredTrack): pass
