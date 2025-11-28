from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from constants.bot_commands import start_command
from keyboards.inline.search import start_search_keyboard

router = Router()


@router.message(Command(start_command))
async def start(
    message: Message,
    state: FSMContext,
):
    await state.clear()
    await message.answer(
        text="Я помогу найти декларации соответствия по названию продукции и изготовителя.",
        reply_markup=start_search_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
