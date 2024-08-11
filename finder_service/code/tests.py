import asyncio
import time

from aiogram import Bot
from aiogram.types import FSInputFile

from finder_service.code.music_finder_service import MusicFinderService, Track


async def test():
    artist = "Eminem"
    title = "Stan"
    duration = 404
    start = time.time()
    url: str
    token = '7249126856:AAGUhXv5c1v5E-eRxlc7D7-j1A9YB1V0uYc'
    bot = Bot(token=token)

    service = MusicFinderService()
    try:
        result = await service.find_track(Track(title, artist, duration))
        if result is not None:
            file = await service.download_track(result, '.')
            await bot.send_audio(chat_id=892098177, audio=FSInputFile(file))

    finally:
        await service.close()
        await bot.session.close()

    print(time.time() - start)

if __name__ == '__main__':
    asyncio.run(test())
