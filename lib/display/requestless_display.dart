import 'package:orbit/track.dart';

abstract class RequestlessDisplay {
  Future<void> show(ColoredTrack track);

  Future<void> showNoTrack();
}
