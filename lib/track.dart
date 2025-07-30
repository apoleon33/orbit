class Artist {
  /// The **MusicBrainz ID (MBID)** for this entity.
  ///
  /// This unique identifier comes from the [MusicBrainz database](https://musicbrainz.org/),
  /// an open-source music encyclopedia. It serves as a universal, unambiguous reference
  /// for artists, albums, tracks, and other musical works.
  ///
  /// In APIs like Last.fm's, using an MBID is the most reliable way to fetch
  /// data for a specific musical entity, ensuring accuracy even when names
  /// are common, spelled differently, or prone to ambiguity.
  final String mbid;
  final String name;

  Artist(this.name, this.mbid);

  Artist.createFromData(Map data)
    : this(data["artist"]["#text"], data["artist"]["mbid"]);

  @override
  String toString() => "name: $name, mbid: $mbid";
}

enum ImageSize { small, medium, large, extralarge }

class Image {
  final ImageSize imageSize;
  final String url;

  Image(this.url, this.imageSize);

  @override
  String toString() => "url: $url, size: $imageSize";
}

class Track {
  final Artist artist;
  final List<Image> image;
  final String name;
  final String url;

  Track(
    this.name, {
    required this.artist,
    required this.image,
    required this.url,
  });

  Track.createFromData(Map data)
    : this(
        data["name"],
        artist: Artist.createFromData(data),
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
