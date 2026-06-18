from sdbus import (DbusInterfaceCommonAsync, dbus_method_async,
                   dbus_property_async, dbus_signal_async, request_default_bus_name_async)

from lib.display.requestless_display import RequestlessDisplay
from lib.track import ColoredTrack


class DbusInterface(DbusInterfaceCommonAsync,
                    interface_name='org.apoleon.orbit'):

    @dbus_signal_async(signal_signature='(ssssssss)')
    def currentTrack(self) -> tuple:
        # name, mbid, artist, album, url, color1, color2, color3; color4, color5
        raise NotImplementedError


class Dbus(RequestlessDisplay):
    exportObject = DbusInterface()

    async def init(self):
        await request_default_bus_name_async('org.apoleon.orbit')
        self.exportObject.export_to_dbus('/')

    @staticmethod
    def convertTrackToDbus(track: ColoredTrack) -> tuple:
        return (
            track.name,
            track.album.name,
            track.artist.name,
            str(track.palette.colors[0].hex),
            str(track.palette.colors[1].hex),
            str(track.palette.colors[2].hex),
            str(track.palette.colors[3].hex),
            str(track.palette.colors[4].hex),
        )

    def show(self, track: ColoredTrack):
        self.exportObject.currentTrack.emit(Dbus.convertTrackToDbus(track))
