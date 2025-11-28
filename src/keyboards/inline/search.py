from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_search_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Найти декларацию",
                callback_data="start_search",
            )
        ],
    ]
)

skip_manufacturer_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Пропустить",
                callback_data="skip_manufacturer",
            )
        ],
    ]
)

confirm_search_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Искать",
                callback_data="confirm_search",
            )
        ],
    ]
)
