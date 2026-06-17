from sdbus import (DbusInterfaceCommonAsync, dbus_method_async,
                   dbus_property_async, dbus_signal_async, request_default_bus_name_async)

from lib.display.requestless_display import RequestlessDisplay
from lib.track import ColoredTrack


class DbusInterface(DbusInterfaceCommonAsync,
                    interface_name='org.apoleon.orbit'):

    @dbus_signal_async(signal_signature='(sssssssssss)')
    def currentTrack(self) -> tuple:
        # name, mbid, artist, album, url, color1, color2, color3; color4, color5
        return NotImplementedError


class Dbus(RequestlessDisplay):
    exportObject = DbusInterface()

    def __int__(self):
        request_default_bus_name_async('org.apoleon.orbit')
        self.exportObject.export_to_dbus('/')

    @staticmethod
    def convertTrackToDbus(track: ColoredTrack) -> tuple:
        return (
            track.name,
            track.mbid,
            track.artist,
            track.album,
            track.url,
            track.palette.colors[0].hex,
            track.palette.colors[1].hex,
            track.palette.colors[2].hex,
            track.palette.colors[3].hex,
            track.palette.colors[4].hex
        )

    def show(self, track: ColoredTrack):
        self.exportObject.currentTrack.emit(Dbus.convertTrackToDbus(track))
