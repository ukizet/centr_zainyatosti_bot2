from aiogram.dispatcher.filters.state import State, StatesGroup


class Add(StatesGroup):
    """Стани для додавання нової вакансії"""
    name = State()
    desc = State()
    salary = State()
