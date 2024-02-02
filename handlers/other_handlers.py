from aiogram import Router
from aiogram.types import Message
from bot.create_bot import bot

router: Router = Router()


@router.message
async def send_echo(message: Message):
    """Handler for any messages that user types to bot"""
    await bot.send_message(
        message.from_user.id,
        text=f'Что за странные каракули "{message.text}".',
    )
