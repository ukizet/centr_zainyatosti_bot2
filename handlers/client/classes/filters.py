from dataclasses import dataclass

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from .button import Button

from create import dp


@dataclass
class Filters(Button):
    """Class for handling filters"""

    def __init__(self):
        self.names = Names()
        self.salaries = Salaries()
        self.drop = Drop(self.names, self.salaries)

        self.button_name = "Фільтри"
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.add_buttons_to_kb()

    async def main(self, message: types.Message):
        """Main handler"""

        await message.answer("Ось фільтри", reply_markup=self.kb)


@dataclass
class Names(Button):
    """Class that represents names button is filters"""

    def __init__(self):
        self.button_name = "Назви вакансій"
        self.states = NamesStates()

    async def add_name(self, message: types.Message):
        """Adds name to names list"""

        # !!! Це треба зробити на машині станів
        if len(self.states.get_names()) >= 10:
            await message.answer("Ви не можете вибрати більше 10 назв вакансій")
            return
        await NamesStates.name.set()
        await message.answer("Введіть назву вакансії яку хочете залишити")

    def get_names(self) -> list:
        """Returns names list"""

        return self.states.get_names()
    
    def clear_names(self):
        """Clears names list"""

        self.states.names.clear()


class NamesStates(StatesGroup):
    """States for names button in filters"""

    name = State()

    def __init__(self):
        self.names = []

    async def name_handler(self, message: types.Message, state: FSMContext):
        """Handler for name state"""

        self.names.append(message.text)
        await state.finish()
        await message.answer(f"self.names: {self.names}")

    def get_names(self) -> list:
        """Returns names list"""

        return self.names


@dataclass
class Salaries(Button):
    """Class that represents salaries button in filters"""

    salaries: list

    def __init__(self):
        self.button_name = "Зарплати"
        self.salaries = []

    async def add_salary(self, message: types.Message):
        """Adds salary to salaries list"""


@dataclass
class Drop(Button):
    """Class that represents drop button in filters"""

    def __init__(self, names: Names, salaries: Salaries):
        self.button_name = "Скинути фільтри"
        self.names = names
        self.salaries = salaries

        dp.register_message_handler(self.drop_filters,
                                    lambda message: message.text == self.button_name)

    async def drop_filters(self, message: types.Message):
        """Drops all filters"""

        self.names.clear_names()
        await message.answer("Фільтри скинуті")
