import 'package:test/test.dart';
import 'package:orbit/track.dart';

void main() {
  group('LastFMEntity', () {
    test('should create entity with name and mbid', () {
      final artist = Artist('Test Artist', 'test-mbid-123');

      expect(artist.name, equals('Test Artist'));
      expect(artist.mbid, equals('test-mbid-123'));
    });

    test('should implement toString correctly', () {
      final artist = Artist('Test Artist', 'test-mbid-123');

      expect(artist.toString(), equals('name: Test Artist, mbid: test-mbid-123'));
    });

    test('should implement equality based on mbid', () {
      final track1 = Track(
        'Test Track',
        'same-mbid',
        artist: Artist('Artist', 'artist-mbid'),
        album: Album('Album', 'album-mbid'),
        image: [],
        url: 'http://test.com',
      );

      final track2 = Track(
        'Different Track',
        'same-mbid',
        artist: Artist('Different Artist', 'different-artist-mbid'),
        album: Album('Different Album', 'different-album-mbid'),
        image: [],
        url: 'http://different.com',
      );

      expect(track1, equals(track2));
    });

    test('should have different hash codes for different mbids', () {
      final track1 = Track(
        'Test Track',
        'mbid-1',
        artist: Artist('Artist', 'artist-mbid'),
        album: Album('Album', 'album-mbid'),
        image: [],
        url: 'http://test.com',
      );

      final track2 = Track(
        'Test Track',
        'mbid-2',
        artist: Artist('Artist', 'artist-mbid'),
        album: Album('Album', 'album-mbid'),
        image: [],
        url: 'http://test.com',
      );

      expect(track1.hashCode, isNot(equals(track2.hashCode)));
    });

    test('should have same hash codes for same mbids', () {
      final track1 = Track(
        'Test Track',
        'same-mbid',
        artist: Artist('Artist', 'artist-mbid'),
        album: Album('Album', 'album-mbid'),
        image: [],
        url: 'http://test.com',
      );

      final track2 = Track(
        'Different Track',
        'same-mbid',
        artist: Artist('Different Artist', 'different-artist-mbid'),
        album: Album('Different Album', 'different-album-mbid'),
        image: [],
        url: 'http://different.com',
      );

      expect(track1.hashCode, equals(track2.hashCode));
    });
  });

  group('Artist', () {
    test('should create artist with name and mbid', () {
      final artist = Artist('Pink Floyd', 'artist-mbid-123');

      expect(artist.name, equals('Pink Floyd'));
      expect(artist.mbid, equals('artist-mbid-123'));
    });

    test('should create artist from API data', () {
      final data = {
        'artist': {
          '#text': 'The Beatles',
          'mbid': 'b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d'
        }
      };

      final artist = Artist.createFromData(data);

      expect(artist.name, equals('The Beatles'));
      expect(artist.mbid, equals('b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d'));
    });

    test('should handle empty mbid in API data', () {
      final data = {
        'artist': {
          '#text': 'Unknown Artist',
          'mbid': ''
        }
      };

      final artist = Artist.createFromData(data);

      expect(artist.name, equals('Unknown Artist'));
      expect(artist.mbid, equals(''));
    });
  });

  group('Album', () {
    test('should create album with name and mbid', () {
      final album = Album('Dark Side of the Moon', 'album-mbid-456');

      expect(album.name, equals('Dark Side of the Moon'));
      expect(album.mbid, equals('album-mbid-456'));
    });

    test('should create album from API data', () {
      final data = {
        'album': {
          '#text': 'Abbey Road',
          'mbid': 'album-mbid-beatles'
        }
      };

      final album = Album.createFromData(data);

      expect(album.name, equals('Abbey Road'));
      expect(album.mbid, equals('album-mbid-beatles'));
    });

    test('should handle empty mbid in API data', () {
      final data = {
        'album': {
          '#text': 'Unknown Album',
          'mbid': ''
        }
      };

      final album = Album.createFromData(data);

      expect(album.name, equals('Unknown Album'));
      expect(album.mbid, equals(''));
    });
  });

  group('ImageSize', () {
    test('should have all expected image sizes', () {
      expect(ImageSize.values, hasLength(4));
      expect(ImageSize.values, contains(ImageSize.small));
      expect(ImageSize.values, contains(ImageSize.medium));
      expect(ImageSize.values, contains(ImageSize.large));
      expect(ImageSize.values, contains(ImageSize.extralarge));
    });

    test('should have correct string representation', () {
      expect(ImageSize.small.name, equals('small'));
      expect(ImageSize.medium.name, equals('medium'));
      expect(ImageSize.large.name, equals('large'));
      expect(ImageSize.extralarge.name, equals('extralarge'));
    });
  });

  group('Image', () {
    test('should create image with url and size', () {
      final image = Image('https://example.com/image.jpg', ImageSize.large);

      expect(image.url, equals('https://example.com/image.jpg'));
      expect(image.imageSize, equals(ImageSize.large));
    });

    test('should implement toString correctly', () {
      final image = Image('https://example.com/image.jpg', ImageSize.medium);

      expect(image.toString(), equals('url: https://example.com/image.jpg, size: ImageSize.medium'));
    });
  });

  group('Track', () {
    test('should create track with all required properties', () {
      final artist = Artist('Test Artist', 'artist-mbid');
      final album = Album('Test Album', 'album-mbid');
      final images = [
        Image('https://example.com/small.jpg', ImageSize.small),
        Image('https://example.com/large.jpg', ImageSize.large),
      ];
      final track = Track(
        'Test Track',
        'track-mbid',
        artist: artist,
        album: album,
        image: images,
        url: 'https://last.fm/track/test',
      );

      expect(track.name, equals('Test Track'));
      expect(track.mbid, equals('track-mbid'));
      expect(track.artist.name, equals(artist.name));
      expect(track.artist.mbid, equals(artist.mbid));
      expect(track.album.name, equals(album.name));
      expect(track.album.mbid, equals(album.mbid));
      expect(track.image, equals(images));
      expect(track.url, equals('https://last.fm/track/test'));
    });

    test('should create track from API data', () {
      final data = {
        'name': 'Bohemian Rhapsody',
        'mbid': 'track-mbid-queen',
        'artist': {
          '#text': 'Queen',
          'mbid': 'artist-mbid-queen'
        },
        'album': {
          '#text': 'A Night at the Opera',
          'mbid': 'album-mbid-queen'
        },
        'image': [
          {
            '#text': 'https://example.com/small.jpg',
            'size': 'small'
          },
          {
            '#text': 'https://example.com/medium.jpg',
            'size': 'medium'
          },
          {
            '#text': 'https://example.com/large.jpg',
            'size': 'large'
          },
          {
            '#text': 'https://example.com/extralarge.jpg',
            'size': 'extralarge'
          }
        ],
        'url': 'https://www.last.fm/music/Queen/_/Bohemian+Rhapsody'
      };

      final track = Track.createFromData(data);

      expect(track.name, equals('Bohemian Rhapsody'));
      expect(track.mbid, equals('track-mbid-queen'));
      expect(track.artist.name, equals('Queen'));
      expect(track.artist.mbid, equals('artist-mbid-queen'));
      expect(track.album.name, equals('A Night at the Opera'));
      expect(track.album.mbid, equals('album-mbid-queen'));
      expect(track.image, hasLength(4));
      expect(track.image[0].url, equals('https://example.com/small.jpg'));
      expect(track.image[0].imageSize, equals(ImageSize.small));
      expect(track.image[1].url, equals('https://example.com/medium.jpg'));
      expect(track.image[1].imageSize, equals(ImageSize.medium));
      expect(track.image[2].url, equals('https://example.com/large.jpg'));
      expect(track.image[2].imageSize, equals(ImageSize.large));
      expect(track.image[3].url, equals('https://example.com/extralarge.jpg'));
      expect(track.image[3].imageSize, equals(ImageSize.extralarge));
      expect(track.url, equals('https://www.last.fm/music/Queen/_/Bohemian+Rhapsody'));
    });

    test('should handle API data with empty images list', () {
      final data = {
        'name': 'Test Track',
        'mbid': 'test-mbid',
        'artist': {
          '#text': 'Test Artist',
          'mbid': 'test-artist-mbid'
        },
        'album': {
          '#text': 'Test Album',
          'mbid': 'test-album-mbid'
        },
        'image': [],
        'url': 'https://example.com/track'
      };

      final track = Track.createFromData(data);

      expect(track.image, isEmpty);
    });

    test('should handle API data with missing mbids', () {
      final data = {
        'name': 'Unknown Track',
        'mbid': '',
        'artist': {
          '#text': 'Unknown Artist',
          'mbid': ''
        },
        'album': {
          '#text': 'Unknown Album',
          'mbid': ''
        },
        'image': [],
        'url': 'https://example.com/unknown'
      };

      final track = Track.createFromData(data);

      expect(track.name, equals('Unknown Track'));
      expect(track.mbid, equals(''));
      expect(track.artist.name, equals('Unknown Artist'));
      expect(track.artist.mbid, equals(''));
      expect(track.album.name, equals('Unknown Album'));
      expect(track.album.mbid, equals(''));
      expect(track.url, equals('https://example.com/unknown'));
    });

    test('should implement toString correctly', () {
      final artist = Artist('Test Artist', 'artist-mbid');
      final album = Album('Test Album', 'album-mbid');
      final images = [Image('https://example.com/image.jpg', ImageSize.small)];
      final track = Track(
        'Test Track',
        'track-mbid',
        artist: artist,
        album: album,
        image: images,
        url: 'https://example.com/track',
      );

      final expected = 'Track name: Test Track \n'
          'Artist name: Test Artist, mbid: artist-mbid \n'
          'url: https://example.com/track \n'
          'images: [url: https://example.com/image.jpg, size: ImageSize.small]';

      expect(track.toString(), equals(expected));
    });

    test('should be equal when mbids are the same', () {
      final track1 = Track(
        'Track 1',
        'same-mbid',
        artist: Artist('Artist 1', 'artist-1'),
        album: Album('Album 1', 'album-1'),
        image: [],
        url: 'https://example.com/1',
      );

      final track2 = Track(
        'Track 2',
        'same-mbid',
        artist: Artist('Artist 2', 'artist-2'),
        album: Album('Album 2', 'album-2'),
        image: [],
        url: 'https://example.com/2',
      );

      expect(track1 == track2, isTrue);
    });

    test('should not be equal when mbids are different', () {
      final track1 = Track(
        'Same Track',
        'mbid-1',
        artist: Artist('Same Artist', 'same-artist'),
        album: Album('Same Album', 'same-album'),
        image: [],
        url: 'https://example.com/same',
      );

      final track2 = Track(
        'Same Track',
        'mbid-2',
        artist: Artist('Same Artist', 'same-artist'),
        album: Album('Same Album', 'same-album'),
        image: [],
        url: 'https://example.com/same',
      );

      expect(track1 == track2, isFalse);
    });
  });
}
