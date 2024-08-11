import os

from finder_service.code.parsers.muzofond_parser import *
from finder_service.code.parsers.krolik_parser import *
from finder_service.code.parsers.parser_factory import *
from finder_service.code.parsers.party_parser import *


class Track:

    def __init__(self, title: str, artist: str, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration


class DownloadableTrack(Track):

    def __init__(self, title: str, artist: str, duration: int, url: str):
        super().__init__(title, artist, duration)
        self.url = url


class MusicFinderService:

    def __init__(self):
        self._session = aiohttp.ClientSession()
        self._parsers = [PartyParser(self._session), MuzofondParser(self._session), KrolikParser(self._session)]
        self._parser_factory = ParserFactory(*self._parsers)

    async def close(self):
        await self._session.close()

    async def find_track(self, track: Track) -> DownloadableTrack | None:
        res = await self._parser_factory.best_match(track.artist, track.title, track.duration)
        if res is None:
            return None
        return DownloadableTrack(track.title, track.artist, track.duration, res.url)

    async def download_track(self, track: DownloadableTrack, path: str) -> str:
        response = await self._session.get(track.url)
        reader = response.content

        file_name = f"{path}/{track.title} - {track.artist}"

        with open(file_name, 'wb') as f:
            f.write(await reader.read())

        return file_name

    @staticmethod
    def delete_track(path):
        os.remove(path)
