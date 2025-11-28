from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.declarations_urls import get_declaration_url


def build_declarations_keyboard(
    declarations: list[dict],
):
    buttons = []
    for declaration in declarations:
        declaration_id = declaration.get("id")

        if not declaration_id:
            continue

        manufacterName = declaration.get("manufacterName", "")
        number = declaration.get("number", "")
        text = f"{manufacterName} – {number}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=text,
                    url=get_declaration_url(declaration_id),
                )
            ]
        )

    if not buttons:
        return None

    return InlineKeyboardMarkup(inline_keyboard=buttons)
