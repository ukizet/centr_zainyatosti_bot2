from dataclasses import dataclass

from aiogram import types
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from create import bot, db


@dataclass
class Button:
    """Base class for buttons"""

    button_name: str
    kb: ReplyKeyboardMarkup

    def __init__(self):
        self.button_name = ""
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)

    def add_buttons_to_kb(self):
        """Adds all buttons from class to class keyboard"""

        for attr_name in self.__dict__:
            attr = getattr(self, attr_name)
            if isinstance(attr, Button):
                self.kb.row(attr.button_name)
            else:
                pass

@dataclass
class Menu(Button):
    """Class for handling menu buttons"""

    page: int
    previous_page: int
    VACANCIES_PER_PAGE: int
    inline_kb: InlineKeyboardMarkup
    all_vacancies: list
    vacs_list: list
    messages_id = list
    chat_id: int

    def __init__(self):
        self.page = 1
        self.previous_page = 0
        self.VACANCIES_PER_PAGE = 5
        self.inline_kb = InlineKeyboardMarkup()\
            .row(InlineKeyboardButton(text="◀️",
                                      callback_data="back"),
                 InlineKeyboardButton(text=f"{self.page}",
                                      callback_data="page"),
                 InlineKeyboardButton(text="▶️",
                                      callback_data="next"))
        self.messages_id = []
        self.vacs_message = ''

        self.filters = Filters()

        self.button_name = "Меню"
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.add_buttons_to_kb()

    async def main(self, message: types.Message = None,
                   callbackQuery: types.CallbackQuery = None):
        await message.answer(text="Ось меню", reply_markup=self.kb)
        await self.display_menu(message, callbackQuery)

    async def display_menu(self, message: types.Message = None,
                           callbackQuery: types.CallbackQuery = None):
        """Цей хендлер відповідає за відображення меню вакансій.

        Спочатку бот відправляє 5 повідомлень з вакансіями, 
        а потім відправляє кнопки для переходу на іншу сторінку."""

        if len(self.filters.names.get_names()) > 0:
            condition = ''
            for i, name in enumerate(self.filters.names.get_names()):
                if i == 0:
                    condition += f"name = '{name}'"
                condition += f" OR name = '{name}'"
                if i == len(self.filters.names.get_names()) - 1:
                    pass

            self.all_vacancies = await db.select_data(message,
                                                      '*',
                                                      'vacancies',
                                                      condition)
            pass
        else:
            self.all_vacancies = await db.select_data(message, '*', 'vacancies')

        self.inline_kb = InlineKeyboardMarkup()\
            .row(InlineKeyboardButton(text="◀️",
                                      callback_data="back"),
                 InlineKeyboardButton(text=f"{self.page}",
                                      callback_data="page"),
                 InlineKeyboardButton(text="▶️",
                                      callback_data="next"))
        
        if callbackQuery is None:
            self.vacs_list = self.all_vacancies[
                self.previous_page * self.VACANCIES_PER_PAGE:
                self.page * self.VACANCIES_PER_PAGE]
            self.vacs_message = ''
            for i in range(len(self.vacs_list)):
                vacancy_info = (
                    f"Назва вакансії: {self.vacs_list[i][2]}\n"
                    f"Опис: {self.vacs_list[i][3]}\n"
                    f"ЗП: {self.vacs_list[i][4]}\n"
                    "\n"
                )

                if i == len(self.vacs_list) - 1:
                    self.vacs_message += vacancy_info
                    test_message = await message.answer(self.vacs_message,
                                                        reply_markup=self.inline_kb)
                    self.messages_id.append(test_message.message_id)
                else:
                    self.vacs_message += vacancy_info
        else:
            self.vacs_message = ''
            for i in range(len(self.vacs_list)):
                vacancy_info = (
                    f"Назва вакансії: {self.vacs_list[i][2]}\n"
                    f"Опис: {self.vacs_list[i][3]}\n"
                    f"ЗП: {self.vacs_list[i][4]}\n"
                    "\n"
                )

                self.vacs_message += vacancy_info
            await bot.edit_message_text(chat_id=callbackQuery.message.chat.id,
                                        message_id=self.messages_id[0],
                                        text=self.vacs_message,
                                        reply_markup=self.inline_kb)

    async def back(self, callbackQuery: types.CallbackQuery):
        """Back button handler"""
        if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
            await callbackQuery.answer("Немає попередніх вакансій")
            return
        if self.page <= 1:
            await callbackQuery.answer("Немає попередніх вакансій")
            return
        self.previous_page = self.page-2
        self.page -= 1

        self.vacs_list = self.all_vacancies[
            self.previous_page * self.VACANCIES_PER_PAGE:
            self.page * self.VACANCIES_PER_PAGE]

        await self.display_menu(callbackQuery=callbackQuery)

    async def pages(self, callbackQuery: types.CallbackQuery):
        """Page button handler"""

        await callbackQuery.answer("Ви вже на цій сторінці")

    async def next(self, callbackQuery: types.CallbackQuery):
        """Next button handler"""

        if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
            await callbackQuery.answer("Немає наступних вакансій")
            return
        
        self.previous_page = self.page
        self.page += 1

        self.vacs_list = self.all_vacancies[
            self.previous_page * self.VACANCIES_PER_PAGE:
            self.page * self.VACANCIES_PER_PAGE]
        
        if len(self.vacs_list) == 0:
            await callbackQuery.answer("Немає наступних вакансій")
            return

        await self.display_menu(callbackQuery=callbackQuery)

@dataclass
class Filters(Button):
    """Class for handling filters"""

    def __init__(self):
        self.names = Names()
        self.salaries = Salaries()
        self.drop = Drop()

        self.button_name = "Фільтри"
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.add_buttons_to_kb()

    async def main(self, message: types.Message):
        """Main handler"""

        await message.answer("Ось фільтри", reply_markup=self.kb)
    
@dataclass
class Names(Button):
    """Class that represents names button is filters"""
    
    names: list

    def __init__(self):
        self.button_name = "Назви вакансій"
        self.names = []

    async def add_name(self, message: types.Message):
        """Adds name to names list"""

        # !!! Це треба зробити на машині станів
        await message.answer("Введіть назву вакансії яку хочете залишити")
        self.names.append(message.text)
        await message.answer("Назва вакансії додана")

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

    def __init__(self):
        self.button_name = "Скинути фільтри"

    async def drop_filters(self, message: types.Message):
        """Drops all filters"""

        await message.answer("Фільтри скинуті")
