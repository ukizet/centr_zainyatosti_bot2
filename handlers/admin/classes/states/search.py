from aiogram.dispatcher.filters.state import State, StatesGroup


class Search(StatesGroup):
    """Стани для пошуку вакансії"""
    name = State()
