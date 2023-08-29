from aiogram import Bot, Dispatcher

from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_COMMANDS
from config_data.config import load_config, Config

config: Config = load_config()

bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()


async def set_main_menu(my_bot: Bot) -> None:
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in LEXICON_COMMANDS.items()
    ]
    await my_bot.set_my_commands(main_menu_commands)
