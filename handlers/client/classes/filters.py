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

        if len(self.states.get_names()) >= 10:
            await message.answer("Ви не можете вибрати більше 10 назв вакансій")
            return
        await self.states.name.set()
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

    def __init__(self):
        self.button_name = "Зарплати"
        self.states = SalariesStates()

        dp.register_message_handler(self.add_salary_range,
                                    lambda message: message.text == self.button_name)
        dp.register_callback_query_handler(self.states.salary_handler, state=self.states.salary)


    async def add_salary_range(self, message: types.Message):
        """Adds salary to salaries list"""

        await self.states.salary.set()
        await message.answer("Введіть діапазон зарплат. В такому форматі: 7000-12000")

    def get_salaries(self) -> str:
        """Returns salaries list"""

        return self.states.get_salary_range()


class SalariesStates(StatesGroup):
    """States for salaries button in filters"""

    salary = State()

    def __init__(self):
        self.salary_range = ""

        

    async def salary_handler(self, message: types.Message, state: FSMContext):
        """Handler for salary state"""

        self.salary_range = message.text
        await state.finish()
        await message.answer(f"self.salary_range: {self.salary_range}")

    def get_salary_range(self) -> str:
        """Returns salary range string"""

        return self.salary_range


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
