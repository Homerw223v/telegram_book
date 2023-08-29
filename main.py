import asyncio
import logging

from datetime import datetime

from database.database_sq import sql_start
from bot.create_bot import dp, bot, set_main_menu
from handlers import other_handlers, client_handlers

logger: logging = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


async def main():
    logger.info(f'Starting bot...')
    await sql_start()
    logger.info('Database connected')
    await set_main_menu(bot)
    logger.info(f"Menu activated")
    dp.include_routers(client_handlers.router, other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Book created')
    logger.info(f'Bot started at {datetime.now()}')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run((main()))
