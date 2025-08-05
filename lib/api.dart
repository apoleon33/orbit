import 'package:dio/dio.dart';
import 'package:orbit/track.dart';

/// A class representing the parameters required for Last.fm API requests.
class Params {
  /// The API key for authenticating requests with the Last.fm API.
  final String apiKey;

  /// The Last.fm username for whom data is requested.
  final String user;

  /// The format of the API response. Possible values are `"json"` (default) or `"xml"` (xml does break the [LastFM] class use).
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

/// A service class for interacting with the Last.fm API to retrieve user track data.
class LastFM {
  final Params params;
  final String baseUrl = "https://ws.audioscrobbler.com/2.0/";
  final Dio dio = Dio();
  LastFM({required this.params});

  /// Makes a GET request to the Last.fm API using the provided parameters.
  /// Returns the response data as a [Map].
  Future<Map> _callApi() async {
    //  (await dio.get("$baseUrl$params")).data;
    Response call = await dio.get("$baseUrl$params");
    if (call.data["error"] != null) {
      throw Exception(
        "Error occured while fetching LastmFM's api: ${call.data["message"]}",
      );
    }

    return call.data;
  }

  /// Checks if the user is currently playing a track on Last.fm.
  Future<bool> isUserNowPlaying() async =>
      (await _callApi())["recenttracks"]["track"][0]["@attr"] != null;

  /// Retrieves the most recent track played by the user.
  /// Returns a [Track] instance.
  Future<Track> getLastTrack() async =>
      Track.createFromData((await _callApi())["recenttracks"]["track"][0]);
}
