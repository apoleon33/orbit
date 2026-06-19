from sdbus import (DbusInterfaceCommonAsync, dbus_method_async,
                   dbus_property_async, dbus_signal_async, request_default_bus_name_async)

from lib.display.requestless_display import RequestlessDisplay
from lib.track import ColoredTrack


class DbusInterface(DbusInterfaceCommonAsync,
                    interface_name='org.apoleon.orbit'):

    track: tuple = tuple("" for i in range(15))

    @dbus_property_async(property_signature=f'(sssssssssssssss)')
    def currentTrack(self) -> tuple:
        if len(self.track) == 15:
            return self.track
        elif len(self.track) > 15:
            return self.track[:15]
        else:
            return self.track + tuple('#000000' for missing in range(15- len(self.track)))


def convertTrackToDbus(track: ColoredTrack) -> tuple:
    return (
        track.name,
        track.album.name,
        track.artist.name,
    ) + tuple(str(color.hex) for color in track.palette.colors)


class Dbus(RequestlessDisplay):
    exportObject = DbusInterface()

    async def init(self):
        await request_default_bus_name_async('org.apoleon.orbit')
        self.exportObject.export_to_dbus('/')

    def show(self, track: ColoredTrack):
        self.exportObject.track = convertTrackToDbus(track)

    def showNotPlaying(self):
        self.exportObject.track = ("No media playing",) + tuple("" for i in range(14))