import 'package:dotenv/dotenv.dart';
import 'package:orbit/api.dart';
import 'package:orbit/display/display_manager.dart';
import 'package:orbit/display/view.dart';

void main() async {
  var env = DotEnv(includePlatformEnvironment: true)..load();
  assert(env.isDefined("API_KEY"));

  final DisplayManager displayManager = DisplayManager(
    LastFM(
      params: Params(apiKey: env["API_KEY"]!, user: "apoleon33"),
    ),
  );

  displayManager.displays.add(
    Interface(
      LastFM(
        params: Params(apiKey: env["API_KEY"]!, user: "apoleon33"),
      ),
    ),
  );

  for (;;) {
    await displayManager.display();
  }
}
