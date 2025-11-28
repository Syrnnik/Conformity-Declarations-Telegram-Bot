from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


def format_summary(
    product: str,
    manufacturer: str,
):
    manufacturer_to_show = manufacturer if manufacturer else "–"
    return f"Продукция: `{product}`\nИзготовитель: `{manufacturer_to_show}`"


async def send_summary(
    message: Message,
    state: FSMContext,
    manufacturer: str,
    reply_markup=None,
):
    data = await state.get_data()
    product = data.get("product")

    if not product:
        await message.answer(
            text="Сначала введите продукцию.",
        )
        return

    await state.update_data(manufacturer=manufacturer)

    summary_text = format_summary(product=product, manufacturer=manufacturer)
    await message.answer(
        text=summary_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )
