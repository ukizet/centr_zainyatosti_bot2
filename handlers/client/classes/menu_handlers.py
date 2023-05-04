from dataclasses import dataclass

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import exceptions
from create import bot, db


@dataclass
class MenuHandlers:
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
        self.chat_id = 0
        self.vacs_message = ''
        
    async def display_menu(self, message: types.Message = None,
                           callbackQuery: types.CallbackQuery = None):
        """Цей хендлер відповідає за відображення меню вакансій.

        Спочатку бот відправляє 5 повідомлень з вакансіями, 
        а потім відправляє кнопки для переходу на іншу сторінку."""

        if self.chat_id == 0:
            self.chat_id = message.chat.id
        else:
            pass

        self.all_vacancies = await db.select_data(message, '*', 'vacancies')

        self.inline_kb = InlineKeyboardMarkup()\
            .row(InlineKeyboardButton(text="◀️",
                                      callback_data="back"),
                 InlineKeyboardButton(text=f"{self.page}",
                                      callback_data="page"),
                 InlineKeyboardButton(text="▶️",
                                      callback_data="next"))

        self.vacs_list = self.all_vacancies[self.previous_page * self.VACANCIES_PER_PAGE: self.page * self.VACANCIES_PER_PAGE]

        if callbackQuery is None:
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
            print()

    async def inline_button_back(self, callbackQuery: types.CallbackQuery):
        """Back button handler"""
        if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
            callbackQuery.answer("Немає попередніх вакансій")
            return
        if self.page <= 1:
            callbackQuery.answer("Немає попередніх вакансій")
            return
        self.previous_page = self.page-2
        self.page -= 1

        await self.display_menu(callbackQuery=callbackQuery)

    async def inline_button_next(self, callbackQuery: types.CallbackQuery):
        """Next button handler"""
        # зробити так щоб ця кнопка змінювала ці 5 вакансій на наступні 5 вакансій

        if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
            callbackQuery.answer("Немає наступних вакансій")
            return
        self.previous_page = self.page
        self.page += 1
        await self.display_menu(callbackQuery=callbackQuery)

        # for id in self.messages_id:
        #     await bot.edit_message_text(chat_id=self.chat_id,
        #                                    message_id=id,
        #                                    text="test",
        #                                    reply_markup=self.inline_kb)
