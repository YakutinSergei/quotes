import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import bot, dp
from data_base import quotes_db
from handlers import apsh, hand_user

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    #Подключаемся к базе данных
    await quotes_db.db_connect()

    # # Регистриуем роутеры в диспетчере
    dp.include_router(hand_user.router)

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(apsh.start_quote, 'cron', hour=14, minute=00)
    scheduler.start()
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())