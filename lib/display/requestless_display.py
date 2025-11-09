from abc import ABC

from lib.led_control.util import ColoredTrack


class RequestlessDisplay(ABC):
    def show(self, track: ColoredTrack): pass
