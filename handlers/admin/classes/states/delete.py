from aiogram.dispatcher.filters.state import State, StatesGroup


class Delete(StatesGroup):
    """Стани для видалення вакансії"""
    name = State()
    id = State()
