import 'dart:io';

import 'package:image/image.dart' as img;
import 'package:orbit/api.dart';
import 'package:orbit/track.dart';
import 'package:tint/tint.dart';

import 'package:http/http.dart' as http;
import 'package:colorgram/colorgram.dart';

class Interface {
  final LastFM api;

  bool? _previousStatus;
  Track? _currentTrack;

  /// The number of colors extracted from the album cover.
  final int colorNUmber = 3;

  /// How many lines the display of the current song takes in the terminal.
  final int nowPLayingLineNumber = 6;

  /// How many lines the "no music detected" text takes in the terminal.
  final int notPlayingLineNumber = 1;

  Interface(this.api);

  /// Clears the previously used lines
  void _overwriteLines(int lines) {
    // Move cursor up by 'lines' rows
    stdout.write('\x1B[${lines}A');
    // Clear from cursor to end of screen
    stdout.write('\x1B[0J');
  }

  // Idk what's happening here honestly it's deepseek
  Future<List<CgColor>?> downloadAndAnalyzeImageMemory(String imageUrl) async {
    try {
      final response = await http.get(Uri.parse(imageUrl));

      if (response.statusCode == 200) {
        // Décoder l'image en mémoire
        img.Image? image = img.decodeImage(response.bodyBytes);

        if (image != null) {
          // Solution temporaire: écrire dans un fichier mémoire
          final tempFile = File('temp_image.jpg');
          await tempFile.writeAsBytes(img.encodeJpg(image));

          List<CgColor> colors = extractColor(tempFile, colorNUmber);

          await tempFile.delete();

          return colors;
        }
      }
    } catch (e) {
      print('Erreur: $e');
      return null;
    }
    return null;
  }

  /// Returns a string colored like the ones given in arguments
  String createColorPalette(List<CgColor> colors) => colors
      .map((color) => "███".rgb(r: color.r, g: color.g, b: color.b))
      .join();

  Future<void> display() async {
    final Track lastTrack = await api.getLastTrack();

    bool nowPlayingStatus = await api.isUserNowPlaying();

    // replace previous lines (probably can be optimized)
    if (lastTrack != _currentTrack) {
      if (_previousStatus != null) {
        if (_previousStatus!) {
          _overwriteLines(nowPLayingLineNumber);
        } else {
          _overwriteLines(notPlayingLineNumber);
        }
      }
    }

    if (nowPlayingStatus) {
      if (lastTrack != _currentTrack) {
        //  reload the whole display only when the track changes

        List<CgColor> dominantColors = (await downloadAndAnalyzeImageMemory(
          lastTrack.image
              .where((img) => img.imageSize == ImageSize.extralarge)
              .toList()[0]
              .url,
        ))!;
        print(
          "${"Music detected!\n".bold()}Name: ${lastTrack.name.italic()}\nAlbum: ${lastTrack.album.name.italic()}\nArtist: ${lastTrack.artist.name.italic()}\nImage: ${lastTrack.image.last.url}\nDominant colors: ${createColorPalette(dominantColors)}"
              .blue(),
        );

        _currentTrack = lastTrack;
      }
    } else {
      print("no music currently playing, retrying in 5s...".bold().blue());
    }

    _previousStatus = nowPlayingStatus;
  }
}
