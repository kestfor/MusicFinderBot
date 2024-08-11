import asyncio

from aiogram.dispatcher.router import Router
from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.callback_data import CallbackData
from confluent_kafka import KafkaException

from bot_service.code.spotify.spotify import AsyncSpotify
from communication_service.sender import Sender
from communication_service.track_task import TrackTask

from finder_service.code.music_finder_service import MusicFinderService, Track

router = Router()
sender = Sender()
spotify = AsyncSpotify()


class AddSongCallbackFactory(CallbackData, prefix="fabAddSong"):
    uri: str


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("введите поисковой запрос 🔎")


@router.callback_query(F.data == "menu")
async def search_track_callback(callback: CallbackQuery):
    await callback.message.edit_text("введите поисковой запрос 🔎")
    await asyncio.sleep(1)
    await callback.message.delete()


@router.message(F.text)
async def search_track_handler(message: Message, state: FSMContext):
    data = {}
    try:
        list_of_results = await spotify.search(message.text)
        request = {}
        keyboard = InlineKeyboardBuilder()
        for item in list_of_results:

            song_info = f'{item.artist} - {item.title}'
            raw_uri = item.id
            request[raw_uri] = song_info

            keyboard.button(text=song_info, callback_data=AddSongCallbackFactory(uri=raw_uri))
            data[raw_uri] = item

        keyboard.adjust(1)
        keyboard.row(InlineKeyboardButton(text='назад', callback_data='menu'))

        await state.set_data(data)
        await message.answer("выберите результат поиска 😊", reply_markup=keyboard.as_markup())
        await message.delete()
    except Exception as e:
        print(e)


@router.callback_query(AddSongCallbackFactory.filter())
async def find_song(callback: CallbackQuery, callback_data: AddSongCallbackFactory, state: FSMContext, bot: Bot):

    raw_uri = callback_data.uri
    data = await state.get_data()
    track = data[raw_uri]

    track_task = TrackTask(raw_uri, track.title, track.artist, track.duration, callback.from_user.id)

    await callback.answer()
    await callback.message.delete()

    try:
        sender.send_task(TrackTask.KAFKA_TOPIC, track_task)
    except KafkaException as e:
        await callback.message.answer('сервис временно не доступен')

    # service = MusicFinderService()
    #
    # try:
    #     result = await service.find_track(track)
    #
    #     if result is None:
    #         await callback.message.edit_text("не смог найти файл(")
    #         return
    #
    #     file_name = await service.download_track(result, "../../data")
    #     await callback.message.edit_text("отправляю")
    #
    #     await bot.send_audio(chat_id=callback.from_user.id, audio=FSInputFile(file_name), title=track.title, performer=track.artist)
    #     await callback.message.delete()
    #     service.delete_track(file_name)
    #
    # except Exception as e:
    #     print(e)
    #     await callback.message.edit_text("произошла ошибка")
    #
    # finally:
    #     await service.close()

