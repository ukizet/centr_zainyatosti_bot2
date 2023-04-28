from dataclasses import dataclass

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
            for i, vac in enumerate(self.vacs_list):
                self.vacancy_info = (
                                    f"Назва вакансії: {vac[2]}\n"
                                    f"Опис: {vac[3]}\n"
                                    f"ЗП: {vac[4]}\n"
                                    )
                
                if i == 4:
                    test_message = await message.answer(self.vacancy_info,
                                                        reply_markup=self.inline_kb)
                else:
                    test_message = await message.answer(self.vacancy_info)
                self.messages_id.append(test_message.message_id)
        else:
            for i2, id in enumerate(self.messages_id):
                # print(f'self.messages_id = {self.messages_id}')
                # print(f'i = {i}')
                if i2 == 4:
                    await bot.edit_message_text(chat_id=self.chat_id,
                                        message_id=id,
                                        text="test",
                                        reply_markup=self.inline_kb)
                else:
                    await bot.edit_message_text(chat_id=self.chat_id,
                                        message_id=id,
                                        text="test")
                # self.messages_id.append(test_message.message_id)

    async def inline_button_back(self, callbackQuery: types.CallbackQuery):
        """Back button handler"""
        if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
            return
        if self.page <= 1:
            return
        self.previous_page = self.page-2
        self.page -= 1

        await self.display_menu(callbackQuery=callbackQuery)

    async def inline_button_next(self, callbackQuery: types.CallbackQuery):
        """Next button handler"""
        # зробити так щоб ця кнопка змінювала ці 5 вакансій на наступні 5 вакансій

        if len(self.all_vacancies) <= self.VACANCIES_PER_PAGE:
            return
        self.previous_page = self.page
        self.page += 1
        await self.display_menu(callbackQuery=callbackQuery)

        # for id in self.messages_id:
        #     await bot.edit_message_text(chat_id=self.chat_id,
        #                                    message_id=id,
        #                                    text="test",
        #                                    reply_markup=self.inline_kb)
