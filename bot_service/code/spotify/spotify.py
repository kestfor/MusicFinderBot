import asyncio
import time

from asyncspotify.client import get_id, Client
from bot_service.code.config_reader import config
import asyncspotify
import asyncspotify.http
from bot_service.code.spotify import spotify_errors


class SpotifySearchResult:

    def __init__(self, title: str, artist: str, id: str, duration: int):
        self.title = title
        self.artist = artist
        self.id = id
        self.duration = duration


class AsyncSpotify:

    _track_prefix = 'spotify%3Atrack%3A'
    _album_prefix = 'spotify:album:'
    _playlist_prefix = 'spotify:playlist:'
    _artist_prefix = 'spotify:artist:'
    _update_timeout = 5
    _volume_step = 5

    def __init__(self):
        self._client_id = config.spotify_client_id.get_secret_value()
        self._client_secret = config.spotify_client_secret.get_secret_value()
        self._spotify_username = config.spotify_username.get_secret_value()

        self._auth = asyncspotify.ClientCredentialsFlow(
            client_id=self._client_id,
            client_secret=self._client_secret,
        )

    @staticmethod
    async def __get_info(item) -> list[SpotifySearchResult]:
        """
        collects artist, track, uri from search request and pack to list
        :param item:
        :return: list of SpotifySearchResult
        """
        res = []
        for i in item["tracks"]:
            res.append(SpotifySearchResult(i.name, i.artists[0].name, i.id, i.duration.seconds))
        return res

    @staticmethod
    def get_full_uri(uri: str):
        if uri.find(AsyncSpotify._track_prefix) == -1:
            return AsyncSpotify._track_prefix + uri

    async def search(self, request: str) -> list[SpotifySearchResult]:
        """
        :param request: запрос
        :return: список с id, автором, названием
        """
        try:
            async with Client(self._auth) as session:
                return await self.__get_info(await session.search("track", q=request, limit=10))
        except:
            raise spotify_errors.ConnectionError
