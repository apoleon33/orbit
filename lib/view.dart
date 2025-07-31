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

  final int colorNUmber = 3;

  Interface(this.api);

  void _overwriteLines(int lines) {
    // Move cursor up by 'lines' rows
    stdout.write('\x1B[${lines}A');
    // Clear from cursor to end of screen
    stdout.write('\x1B[0J');
  }

  Future<List<CgColor>?> downloadAndAnalyzeImageMemory(String imageUrl) async {
    try {
      final response = await http.get(Uri.parse(imageUrl));

      if (response.statusCode == 200) {
        // Décoder l'image en mémoire
        img.Image? image = img.decodeImage(response.bodyBytes);

        if (image != null) {
          // Convertir en format attendu par ColorGram (nécessite adaptation)
          // Note: Cette partie dépend de comment ColorGram attend les données
          // Vous pourriez besoin d'écrire dans un buffer mémoire

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
          _overwriteLines(6);
        } else {
          _overwriteLines(1);
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
