import requests

from lib.track import Track


class Params:
    apiKey: str

    user: str

    format: str
    method: str

    def __init__(self, apiKey, user, format="json", method="user.getrecenttracks"):
        self.apiKey = apiKey
        self.user = user
        self.format = format
        self.method = method

    def __str__(self):
        return f"?api_key={self.apiKey}&method={self.method}&user={self.user}&format={self.format}"


class LastFM:
    params: Params

    baseUrl: str = "https://ws.audioscrobbler.com/2.0/"

    totalScrobbles: str | None

    def __init__(self, params: Params):
        self.params = params

    def _callApi(self) -> dict:
        call = requests.get(f"{self.baseUrl}{self.params}").json()

        if "error" in call:
            raise RuntimeError(f"Error occured while fetching LastmFM's api: {call['message']}")

        self.totalScrobbles = call["recenttracks"]["@attr"]["total"]

        return call

    def isUserNowPlaying(self) -> bool:
        """Check if the user is currently playing a track on Last.fm"""
        apiCall = self._callApi()
        return "@attr" in apiCall["recenttracks"]["track"][0]

    def getLastTrack(self) -> Track:
        """Retrieves the most recent track played by the user."""
        return Track.createFromData(self._callApi()["recenttracks"]["track"][0])

    @property
    def username(self): return self.params.user

    @property
    def totalScrobbles(self): return self.totalScrobbles if self.totalScrobbles is not None else \
    self._callApi()["recenttracks"]["@attr"]["total"]
