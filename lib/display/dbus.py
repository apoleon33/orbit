from lib.display.requestless_display import RequestlessDisplay
from lib.track import ColoredTrack

import logging
import threading


log = logging.getLogger(__name__)


class Dbus(RequestlessDisplay):
	"""Expose the currently shown ColoredTrack over D-Bus.

	This implementation uses sdbus (python-sdbus) when available. If the dependency is
	missing the class becomes a no-op but remains importable.
	"""

	def __init__(self):
		# lazy import of sdbus; keep object usable even if sdbus is not installed
		# (useful for environments without desktop/session bus)
		try:
			from sdbus import ServiceInterface, method, on_signal_ready
			from sdbus.bus import SDBusConnection

			self._ServiceInterface = ServiceInterface
			self._method = method
			self._SDBusConnection = SDBusConnection
			self._on_signal_ready = on_signal_ready
			self._dbus_available = True
		except Exception as e:
			log.debug("sdbus not available: %s", e)
			self._dbus_available = False

		self._server_thread = None
		self._interface = None

		# stored track fields (kept simple primitives so D-Bus methods can return them)
		self._name = ""
		self._artist = ""
		self._album = ""
		self._image_urls = []
		self._url = ""
		self._palette = []

	def _palette_to_hex(self, palette) -> list:
		"""Convert a Pylette.Palette to a list of hex color strings (#RRGGBB).

		The code is defensive: if the palette doesn't match the expected
		structure, return an empty list instead of raising.
		"""
		try:
			hexes = []
			for color in palette.colors:
				# color.rgb is expected to be a tuple (r, g, b, [a]) or (r,g,b)
				rgb = getattr(color, "rgb", None)
				if not rgb:
					continue
				r, g, b = rgb[0], rgb[1], rgb[2]
				hexes.append("#{:02x}{:02x}{:02x}".format(r, g, b))
			return hexes
		except Exception:
			return []

	def _ensure_server(self):
		if not self._dbus_available:
			log.debug("sdbus not available, Dbus.show will be a no-op")
			return False

		if self._server_thread and self._server_thread.is_alive():
			return True

		# create service interface class dynamically so it can capture self
		ServiceInterface = self._ServiceInterface
		method_decorator = self._method

		class TrackInterface(ServiceInterface):
			INTERFACE_NAME = "fr.apoleon33.orbit.Track"

			def __init__(self, parent):
				super().__init__()
				self._parent = parent

			@method_decorator()
			def GetName(self) -> str:
				"""Get the name of the current track."""
				return self._parent._name

			@method_decorator()
			def GetArtist(self) -> str:
				"""Get the artist of the current track."""
				return self._parent._artist

			@method_decorator()
			def GetAlbum(self) -> str:
				"""Get the album of the current track."""
				return self._parent._album

			@method_decorator()
			def GetImageUrls(self) -> list:
				"""Get the image URLs of the current track."""
				return self._parent._image_urls

			@method_decorator()
			def GetUrl(self) -> str:
				"""Get the URL of the current track."""
				return self._parent._url

			@method_decorator()
			def GetPalette(self) -> list:
				"""Get the hex color palette of the current track."""
				return self._parent._palette

		self._TrackInterfaceClass = TrackInterface

		# start the D-Bus server in a background thread
		def _run():
			try:
				bus = self._SDBusConnection().bus
				self._interface = TrackInterface(self)
				bus.export("/fr/apoleon33/orbit/Track", self._interface)
				try:
					bus.request_name("fr.apoleon33.orbit")
				except Exception:
					# if requesting name fails (e.g. running on non-session bus)
					log.debug("could not request dbus name, continuing without claiming it")
				# keep running until program exits
				bus.wait()
			except Exception as e:
				log.debug("dbus server stopped: %s", e)

		self._server_thread = threading.Thread(target=_run, daemon=True)
		self._server_thread.start()
		return True

	def show(self, track: ColoredTrack):
		"""Expose the provided ColoredTrack over D-Bus.

		The object provides simple getter methods over D-Bus for the main fields
		(name, artist, album, image urls, url and palette represented as hex
		strings).
		"""
		if not self._dbus_available:
			return

		self._name = track.name or ""
		self._artist = track.artist.name if getattr(track, "artist", None) else ""
		self._album = track.album.name if getattr(track, "album", None) else ""
		self._image_urls = [img.url for img in getattr(track, "images", []) if getattr(img, "url", None)]
		self._url = track.url or ""
		self._palette = self._palette_to_hex(getattr(track, "palette", []))

		# start server if needed
		self._ensure_server()

	def showNotPlaying(self):
		# clear the exposed object
		self._name = ""
		self._artist = ""
		self._album = ""
		self._image_urls = []
		self._url = ""
		self._palette = []
