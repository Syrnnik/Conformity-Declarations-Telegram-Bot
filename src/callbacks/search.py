from aiogram import F, Router
from aiogram.enums import ChatAction, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.declarations import build_declarations_keyboard
from keyboards.inline.search import confirm_search_keyboard
from states.search_declaration import SearchDeclarationState
from utils.api.declarations import get_declarations
from utils.summary import format_summary, send_summary

router = Router()


@router.callback_query(F.data == "start_search")
async def start_search(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(SearchDeclarationState.product)
    await callback.message.answer(
        text="Напишите название продукции:",
    )
    await callback.answer()


@router.callback_query(F.data == "skip_manufacturer")
async def skip_manufacturer(
    callback: CallbackQuery,
    state: FSMContext,
):
    await send_summary(
        message=callback.message,
        state=state,
        manufacturer="",
        reply_markup=confirm_search_keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_search")
async def confirm_search(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = await state.get_data()
    product = data.get("product")
    manufacturer = data.get("manufacturer", "")

    if not product:
        await callback.answer(
            text="Сначала введите продукцию.",
            show_alert=True,
        )
        return

    await callback.answer()
    await callback.bot.send_chat_action(
        chat_id=callback.message.chat.id,
        action=ChatAction.TYPING,
    )

    declarations_list = await get_declarations(
        manufacturer=manufacturer,
        product=product,
    )

    if not declarations_list:
        summary_text = format_summary(
            product=product,
            manufacturer=manufacturer,
        )
        await callback.message.answer(
            text=f"Не удалось найти ни одной декларации по таким фильтрам:\n{summary_text}",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        keyboard = build_declarations_keyboard(declarations_list)
        await callback.message.answer(
            text="Вот что удалось найти:",
            reply_markup=keyboard,
        )

    await state.clear()
