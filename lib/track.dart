class Artist {
  final String mbid;
  final String name;

  Artist(this.name, this.mbid);

  Artist.createFromData(Map data)
    : this(data["artist"]["#text"], data["artist"]["mbid"]);
}

enum ImageSize { small, medium, large, extralarge }

class Image {
  final ImageSize imageSize;
  final String url;

  Image(this.url, this.imageSize);
}

class Track {
  // {artist: {mbid: bf629fc0-2d07-4fa3-90dd-1e77629be935, #text: Twin Tribes}, streamable: 0, image: [{size: small, #text: https://lastfm.freetls.fastly.net/i/u/34s/e1c3d18e5e232def118fd0a40da8382c.png}, {size: medium, #text: https://lastfm.freetls.fastly.net/i/u/64s/e1c3d18e5e232def118fd0a40da8382c.png}, {size: large, #text: https://lastfm.freetls.fastly.net/i/u/174s/e1c3d18e5e232def118fd0a40da8382c.png}, {size: extralarge, #text: https://lastfm.freetls.fastly.net/i/u/300x300/e1c3d18e5e232def118fd0a40da8382c.png}], mbid: 578e39d7-d6b0-4a10-ac33-9364432f4906, album: {mbid: , #text: Monolith - Single}, name: Monolith, @attr: {nowplaying: true}, url: https://www.last.fm/music/Twin+Tribes/_/Monolith}
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
            .map((elem) => Image(elem["#text"], ImageSize.small))
            .toList(),
        url: data["url"],
      );
}
