import asyncio

from communication_service.track_task import TrackTask
from config_reader import config
from aiogram import Bot, Dispatcher
from handlers import router
from confluent_kafka.admin import AdminClient, NewTopic


admin_client = AdminClient({
    "bootstrap.servers": "localhost:9092"
})

topic_list = [NewTopic(TrackTask.KAFKA_TOPIC, 1, 1)]
admin_client.create_topics(topic_list)

#logging.basicConfig(level=logging.WARNING, filename='../bot_log.log', filemode='w')


async def main():

    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    token = config.bot_token.get_secret_value()
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(router)
    print("started")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
