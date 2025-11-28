from aiogram.fsm.state import State, StatesGroup


class SearchDeclarationState(StatesGroup):
    product = State()
    manufacturer = State()
