import 'dart:io';

import 'package:dotenv/dotenv.dart';
import 'package:orbit/api.dart';
import 'package:orbit/track.dart';

void main() async {
  var env = DotEnv(includePlatformEnvironment: true)..load();
  assert(env.isDefined("API_KEY"));
  final LastFM api = LastFM(
    params: Params(apiKey: env["API_KEY"]!, user: "apoleon33"),
  );
  while (true) {
    Track lastTrack = await api.getLastTrack();

    bool nowPlayingStatus = await api.isUserNowPlaying();
    if (nowPlayingStatus) {
      print("Music detected! currently playing: \n$lastTrack");
    } else {
      print("no music currently playing, retrying in 5s...");
    }

    sleep(Duration(seconds: 5));
  }
}
