from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from database import db_func_sql
from filters.filters import (
    is_digit_callback_data,
    is_del_bookmark_callback_data,
)
from keyboards.bookmarks_kb import (
    create_edit_keyboard,
    create_bookmarks_keyboard,
)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_ru import LEXICON
from services.services import book
from bot.create_bot import bot

router: Router = Router()


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """Handler for command 'start'"""
    user_id = message.from_user.id
    username = message.from_user.username
    await bot.send_message(message.from_user.id, text=LEXICON['/start'])
    if not await db_func_sql.get_user(user_id):
        await db_func_sql.create_reader(user_id, username)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """Handler for command 'help'"""
    await bot.send_message(message.from_user.id, text=LEXICON['/help'])


@router.message(Command(commands=['beginning']))
async def process_beginning_command(message: Message):
    """Handler for command 'beginning'"""
    user_id = message.from_user.id
    page = await db_func_sql.set_page(user_id)
    if not page:
        await db_func_sql.create_reader(user_id, message.from_user.username)
        page = 1

    text = book[page]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward', f'{page}/{len(book)}', 'forward'
        ),
    )


@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    """Handler for command 'continue'"""
    page = await db_func_sql.get_page(message.from_user.id)
    if page:
        text = book[page]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward', f'{page}/{len(book)}', 'forward'
            ),
        )
    else:
        await bot.send_message(message.from_user.id, text=LEXICON['no_user'])


@router.message(Command(commands=['bookmarks']))
async def process_bookmarks_command(message: Message):
    """Handler for command 'bookmarks'"""
    bookmarks = await db_func_sql.get_user_bookmarks(message.from_user.id)
    if bookmarks:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(*bookmarks),
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    """Callback handler for data 'forward'"""
    page = await db_func_sql.get_page(callback.from_user.id)
    if page < len(book):
        await db_func_sql.set_page(callback.from_user.id, page=page + 1)
        text = book[page + 1]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward', f'{page + 1}/{len(book)}', 'forward'
            ),
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    """Callback handler for data 'backward'"""
    page = await db_func_sql.get_page(callback.from_user.id)
    if page > 1:
        await db_func_sql.set_page(callback.from_user.id, page=page - 1)
        text = book[page - 1]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward', f'{page - 1}/{len(book)}', 'forward'
            ),
        )
    await callback.answer()


@router.callback_query(
    lambda x: '/' in x.data and x.data.replace('/', '').isdigit()
)
async def process_page_press(callback: CallbackQuery):
    """Callback handler for data 'xxx/xxx' to add bookmark"""
    user_id = callback.from_user.id
    page = int(callback.data.split('/')[0])
    await db_func_sql.add_bookmark(user_id, page)
    await callback.answer(LEXICON['bookmark_added'])


@router.callback_query(is_digit_callback_data)
async def process_bookmark_press(callback: CallbackQuery):
    """Callback handler uf user tab on bookmark"""
    user_id = callback.from_user.id
    page = int(callback.data)
    text = book[page]
    await db_func_sql.set_page(user_id, page)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward', f'{page}/{len(book)}', 'forward'
        ),
    )
    await callback.answer()


@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    """Callback handler for editing bookmarks"""
    user_id = callback.from_user.id
    bookmarks = await db_func_sql.get_user_bookmarks(user_id)
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(*bookmarks),
    )
    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    """Callback handler for 'cancel' data"""
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(is_del_bookmark_callback_data)
async def process_del_bookmark_press(callback: CallbackQuery):
    """Callback handler for deleting bookmark"""
    page = int(callback.data.replace('del', ''))
    await db_func_sql.delete_bookmark(callback.from_user.id, page)
    bookmarks = await db_func_sql.get_user_bookmarks(callback.from_user.id)
    if bookmarks:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(*bookmarks),
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
