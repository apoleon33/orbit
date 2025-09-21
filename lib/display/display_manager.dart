import 'dart:io';

import 'package:orbit/display/display.dart';
import 'package:orbit/display/requestless_display.dart';
import 'package:orbit/track.dart';

class DisplayManager extends Display {
  List<RequestlessDisplay> displays = List.empty();

  final int delay;

  DisplayManager(super.api, {this.delay = 15});

  @override
  Future<void> display() async {
    final Track lastTrack = await api.getLastTrack();

    for (var display in displays) {
      display.show(
        ColoredTrack.createFromTrack(
          lastTrack,
          (await getColorPalette(lastTrack.url))!,
        ),
      );
    }

    sleep(Duration(seconds: delay));
  }
}
