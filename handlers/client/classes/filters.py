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
        self.drop = Drop(self, self.names, self.salaries)

        self.button_name = "Фільтри"
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.add_buttons_to_kb()

        self.condition = ''
        self.old_names = []
        self.EMPTY = ''

    async def main(self, message: types.Message):
        """Main handler"""

        await message.answer("Ось фільтри", reply_markup=self.kb)

    async def get_condition(self, message: types.Message) -> str:
        """Returns condition"""

        await self.create_condition(message)

        return self.condition
    
    async def create_condition(self, message: types.Message):
        """Creates condition"""

        
        if len(self.names.get_names()) > 0:
            if self.old_names == self.names.get_names():
                pass
            else:
                for i, name in enumerate(self.names.get_names()):
                    # if i == 0 and self.condition == '':
                    #     self.condition = f"name = '{name}'"
                    # elif self.condition != '' and self.condition != f"name = '{name}'" and i == 0:
                    #     self.condition += f" AND name = '{name}'"
                    # elif i > 0:
                    #     self.condition += f" OR name = '{name}'"
                    # else:
                    #     pass
                    if i == 0 and self.condition == self.EMPTY:
                        self.condition = f"name = '{name}'"
                    if self.condition != self.EMPTY and "name" not in self.condition:
                        self.condition += f" AND name = '{name}'"
                    if i > 0 and name not in self.condition:
                        self.condition += f" OR name = '{name}'"
                    if name not in self.old_names:
                        self.old_names.append(name)
        else:
            pass

        if self.salaries.get_salary_range() == '':
            pass
        elif len(self.salaries.get_salary_range().split("-")) == 2:
            min_salary, max_salary = self.salaries.get_salary_range().split("-")
            if self.condition == self.EMPTY:
                self.condition = f"salary BETWEEN {min_salary} AND {max_salary}"
            if self.condition != self.EMPTY and "salary" not in self.condition:
                self.condition += f" AND salary BETWEEN {min_salary} AND {max_salary}"
        else:
            await message.answer("Неправильний формат зарплати")
        pass

    def clear_condition(self): 
        """Clears condition"""

        self.condition = ''
        self.old_names = []


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
        await Filters().create_condition(message)

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
        dp.register_message_handler(self.states.salary_handler, state=self.states.salary)


    async def add_salary_range(self, message: types.Message):
        """Adds salary to salaries list"""

        await self.states.salary.set()
        await message.answer("Введіть діапазон зарплат. В такому форматі: 7000-12000")

    def get_salary_range(self) -> str:
        """Returns salary range string"""

        return self.states.get_salary_range()
    
    def clear_salary_range(self):
        """Clears salary range string"""

        self.states.clear_salary_range()


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
    
    def clear_salary_range(self):
        """Clears salary range string"""

        self.salary_range = ""


@dataclass
class Drop(Button):
    """Class that represents drop button in filters"""

    def __init__(self, filters: Filters, names: Names, salaries: Salaries):
        self.button_name = "Скинути фільтри"
        self.filters = filters
        self.names = names
        self.salaries = salaries

        dp.register_message_handler(self.drop_filters,
                                    lambda message: message.text == self.button_name)

    async def drop_filters(self, message: types.Message):
        """Drops all filters"""

        self.filters.clear_condition()
        self.names.clear_names()
        self.salaries.clear_salary_range()
        await message.answer("Фільтри скинуті")
