from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON


def create_pagination_keyboard(*buttons) -> InlineKeyboardMarkup:
    """Create inline keyboard to see current page and add bookmark"""
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=LEXICON.get(button, button), callback_data=button
            )
            for button in buttons
        ]
    )
    return kb_builder.as_markup()
