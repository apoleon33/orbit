import 'package:dio/dio.dart';
import 'package:orbit/track.dart';

class Params {
  final String apiKey;
  final String user;
  final String format;
  final String method;

  Params({
    required this.apiKey,
    required this.user,
    this.format = "json",
    this.method = "user.getrecenttracks",
  });

  @override
  String toString() =>
      "?api_key=$apiKey&method=$method&user=$user&format=$format";
}

class LastFM {
  final Params params;
  final String baseUrl = "https://ws.audioscrobbler.com/2.0/";
  final Dio dio = Dio();

  LastFM({required this.params});

  Future<Map> _callApi() async => (await dio.get("$baseUrl$params")).data;

  Future<bool> isUserNowPlaying() async =>
      (await _callApi())["recenttracks"]["track"][0]["@attr"] != null;

  Future<Track> getLastTrack() async =>
      Track.createFromData((await _callApi())["recenttracks"]["track"][0]);
}
