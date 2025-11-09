from abc import ABC
from enum import Enum

from Pylette import Palette


class LastFMEntity(ABC):
    """
    An abstract class that represent what LastFM "entities" (track, albums, artists...) have in common.
    """

    mbid: str
    "The **MusicBrainz ID (MBID)** for this entity. This unique identifier comes from the [MusicBrainz database](https://musicbrainz.org/), an open-source music encyclopedia."

    name: str

    def __init__(self, mbid, name):
        self.mbid = mbid
        self.name = name

    def __eq__(self, __value):
        assert type(__value) is Track, "Only Track to Track comparison implemented atm"
        return __value.mbid == self.mbid

    def __str__(self):
        return f"name: {self.name}, mbid: {self.mbid}"


class Artist(LastFMEntity):
    def __init__(self, mbid, name):
        super().__init__(mbid, name)

    @staticmethod
    def createFromData(data: dict):
        return Artist(data["artist"]["#text"], data["artist"]["mbid"])


class Album(LastFMEntity):
    def __init__(self, mbid, name):
        super().__init__(mbid, name)

    @staticmethod
    def createFromData(data: dict):
        return Album(data["album"]["mbid"], data["album"]["name"])


class ImageSize(Enum):
    small = 1
    medium = 2
    large = 3
    extraLarge = 4


class Image:
    imageSize: ImageSize
    url: str

    def __init__(self, imageSize: ImageSize, url):
        self.imageSize = imageSize
        self.url = url

    def __str__(self):
        return f"url: {self.url}, size: {self.imageSize}"


class Track(LastFMEntity):
    artist: Artist
    album: Album
    images: list[Image]
    url: str

    def __init__(self, name, mbid, artist: Artist, album: Album, images: list[Image], url: str):
        super().__init__(mbid, name)
        self.artist = artist
        self.album = album
        self.images = images
        self.url = url

    @staticmethod
    def createFromData(data: dict):
        imageList = []
        for image in data["images"]:
            imageList.append(
                Image(
                    image["#text"],
                    ImageSize.extraLarge
                )
            )

        return Track(data["name"], data["mbid"], Artist.createFromData(data), Album.createFromData(data), imageList)


class ColoredTrack(Track):
    palette: Palette

    def __init__(self, name, mbid, palette, artist, album, images, url):
        super().__init__(name, mbid, artist, album, images, url)

        self.palette = palette

    @staticmethod
    def createFromTrack(track: Track, palette: Palette):
        return ColoredTrack(name=track.name, mbid=track.mbid, palette=palette, artist=track.artist, album=track.album,
                            images=track.images, url=track.url )
