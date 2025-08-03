import 'dart:io';

import 'package:colorgram/colorgram.dart';
import 'package:http/http.dart' as http;
import 'package:image/image.dart' as img;
import 'package:orbit/api.dart';

/// Abstract class for the multiples way of displaying the infos from the api (in a terminal, on a led strip...)
abstract class Display {
  final LastFM api;

  /// The number of colors extracted from the album cover.
  final int colorNUmber = 3;

  Display(this.api);

  Future<List<CgColor>?> getColorPalette(String imageUrl) async {
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

  Future<void> display();
}
