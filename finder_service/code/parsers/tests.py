import time

import requests
from muzofond_parser import *
from krolik_parser import *
from parser_factory import *
from party_parser import *
from finder_service.code.parsers.music_parser import headers


async def test():
    artist = "Eminem"
    title = "Stan"
    duration = 404
    start = time.time()
    url: str
    async with aiohttp.ClientSession(headers=headers) as session:
        parser1 = PartyParser(session)
        parser3 = MuzofondParser(session)
        parser4 = KrolikParser(session)
        factory = ParserFactory(parser1)
        tasks = []
        for i in range(1):
            tasks.append(asyncio.create_task(factory.best_match(artist, title, duration)))
        for task in tasks:
            await task
            print(task.result())
            url = task.result()
    print(time.time() - start)

    if url is not None:
        doc = requests.get(url, params={"Referer": "https://muzyet.net/"})
        with open(f"{title} {artist}.mp3", 'wb') as f:
            f.write(doc.content)


if __name__ == '__main__':
    asyncio.run(test())