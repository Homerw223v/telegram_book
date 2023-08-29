from aiogram.types import CallbackQuery


async def is_digit_callback_data(callback: CallbackQuery) -> bool:
    """Filter for checking if callback is digit
    :param callback: Callback from telegram
    :type callback: CallbackQuery
    :rtype: bool
    :return: If callback is digit
    """
    return isinstance(callback.data, str) and callback.data.isdigit() and len(callback.data) < 4


async def is_del_bookmark_callback_data(callback: CallbackQuery) -> bool:
    """Filter for checking if callback contains del and without 'del' callback is digit
    :param callback: Callback from telegram
    :type callback: CallbackQuery
    :rtype: bool
    :return: If callback contains del and without 'del' callback is digit
    """
    return isinstance(callback.data, str) and 'del' \
        in callback.data and callback.data.replace('del', '').isdigit()


async def is_callback_for_adding_bookmark(callback: CallbackQuery) -> bool:
    """Filter for checking if callback equal xxx/xxx
    :param callback: Callback from telegram
    :type callback: CallbackQuery
    :rtype: bool
    :return: If callback equal xxx/xxx
    """
    return '/' in callback.data and callback.data.replace('/', '').isdigit()
