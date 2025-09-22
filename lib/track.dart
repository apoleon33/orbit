import 'package:colorgram/colorgram.dart';

/// An abstract class that represent what LastFM "entities" (track, albums, artists...) have in common.
abstract class LastFMEntity {
  /// The **MusicBrainz ID (MBID)** for this entity.
  ///
  /// This unique identifier comes from the [MusicBrainz database](https://musicbrainz.org/),
  /// an open-source music encyclopedia.
  final String mbid;
  final String name;

  LastFMEntity(this.name, this.mbid);

  @override
  bool operator ==(Object other) {
    assert(
      other.runtimeType == Track,
      "Only Track to Track comparison implemented atm",
    );
    return (other as Track).mbid == mbid;
  }

  @override
  int get hashCode => mbid.hashCode;

  @override
  String toString() => "name: $name, mbid: $mbid";
}

class Artist extends LastFMEntity {
  Artist(super.name, super.mbid);

  Artist.createFromData(Map data)
    : this(data["artist"]["#text"], data["artist"]["mbid"]);
}

class Album extends LastFMEntity {
  Album(super.name, super.mbid);

  Album.createFromData(Map data)
    : this(data["album"]["#text"], data["album"]["mbid"]);
}

enum ImageSize { small, medium, large, extralarge }

class Image {
  final ImageSize imageSize;
  final String url;

  Image(this.url, this.imageSize);

  @override
  String toString() => "url: $url, size: $imageSize";
}

class Track extends LastFMEntity {
  final Artist artist;
  final Album album;
  final List<Image> image;
  final String url;

  Track(
    super.name,
    super.mbid, {
    required this.artist,
    required this.album,
    required this.image,
    required this.url,
  });

  Track.createFromData(Map data)
    : this(
        data["name"],
        data["mbid"],
        artist: Artist.createFromData(data),
        album: Album.createFromData(data),
        image: (data["image"] as List)
            .map(
              (elem) => Image(
                elem["#text"],
                ImageSize.values.firstWhere(
                  (size) => size.name == elem["size"],
                ),
              ),
            )
            .toList(),
        url: data["url"],
      );

  @override
  String toString() =>
      "Track name: $name \nArtist $artist \nurl: $url \nimages: $image";
}

/// the [Track] class, but with also the color palette of the album.
class ColoredTrack extends Track {
  final List<CgColor> palette;
  ColoredTrack(
    super.name,
    super.mbid,
    this.palette, {
    required super.artist,
    required super.album,
    required super.image,
    required super.url,
  });

  ColoredTrack.createFromTrack(Track track, List<CgColor> palette)
    : this(
        track.name,
        track.mbid,
        palette,
        artist: track.artist,
        album: track.album,
        image: track.image,
        url: track.url,
      );
}
