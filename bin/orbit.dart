import 'dart:io';

import 'package:dotenv/dotenv.dart';
import 'package:orbit/api.dart';
import 'package:orbit/view.dart';

void main() async {
  var env = DotEnv(includePlatformEnvironment: true)..load();
  assert(env.isDefined("API_KEY"));
  final Interface interface = Interface(
    LastFM(
      params: Params(apiKey: env["API_KEY"]!, user: "apoleon33"),
    ),
  );

  while (true) {
    await interface.display();
    sleep(Duration(seconds: 5));
  }
}
