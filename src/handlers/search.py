from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.inline.search import confirm_search_keyboard, skip_manufacturer_keyboard
from states.search_declaration import SearchDeclarationState
from utils.summary import send_summary

router = Router()


@router.message(SearchDeclarationState.product, F.text)
async def handle_product(
    message: Message,
    state: FSMContext,
):
    product = message.text.strip()

    if not product:
        await message.answer(
            text="Название продукции не может быть пустым. Попробуйте ещё раз.",
        )
        return

    await state.update_data(product=product)
    await state.set_state(SearchDeclarationState.manufacturer)
    await message.answer(
        text="Напишите название изготовителя или нажмите «Пропустить».",
        reply_markup=skip_manufacturer_keyboard,
    )


@router.message(SearchDeclarationState.manufacturer, F.text)
async def handle_manufacturer(
    message: Message,
    state: FSMContext,
):
    await send_summary(
        message=message,
        state=state,
        manufacturer=message.text.strip(),
        reply_markup=confirm_search_keyboard,
    )
