from aiogram import Bot, Dispatcher

from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_COMMANDS
from config_data.config import settings

bot: Bot = Bot(token=settings.token)
dp: Dispatcher = Dispatcher()


async def set_main_menu(my_bot: Bot) -> None:
    """Create menu for bot.

    Args:
        my_bot (Bot): Bot object.
    """
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS.items()
    ]
    await my_bot.set_my_commands(main_menu_commands)
