from aiogram import Bot
from aiogram.types import FSInputFile

from communication_service.receiver import Receiver
from communication_service.track_task import TrackTask
from finder_service.code.music_finder_service import MusicFinderService, Track


class Service:
    KAFKA_TOPIC: str = "track_task"
    BOT_TOKEN = "7249126856:AAGUhXv5c1v5E-eRxlc7D7-j1A9YB1V0uYc"

    def __init__(self):
        self._find_service = MusicFinderService()
        self._bot = Bot(token=self.BOT_TOKEN)
        self._receiver = Receiver(self.KAFKA_TOPIC)

    async def run(self):
        print("running")
        while True:
            try:
                track_task: TrackTask = self._receiver.receive()
                print(f"received track task {track_task.track_id}")
                chat_id = track_task.chat_id
                msg = await self._bot.send_message(chat_id=chat_id, text="ищу трек")

                downloadable_track = await self._find_service.find_track(
                    Track(track_task.title, track_task.artist, track_task.duration))

                if downloadable_track is None:
                    await self._bot.edit_message_text(chat_id=chat_id, text="не смог найти файл(",
                                                      message_id=msg.message_id)
                    continue

                await self._bot.edit_message_text(chat_id=chat_id, text="отправляю", message_id=msg.message_id)
                filename = await self._find_service.download_track(downloadable_track, "../data")
                await self._bot.send_audio(audio=FSInputFile(filename), title=track_task.title,
                                           performer=track_task.artist, chat_id=chat_id)
                await self._bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

                self._find_service.delete_track(filename)

            except InterruptedError as interrupted:
                print(interrupted)
                await self._find_service.close()
                await self._receiver.close()
                await self._bot.session.close()
                break

            except Exception as e:
                print(e)
