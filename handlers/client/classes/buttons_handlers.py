from aiogram import types

from dataclasses import dataclass

from keyboards import admin, start
# from command_menu_handlers import CommandMenuHandlers
from .menu_handlers import Menu


@dataclass
class ButtonsHandlers:
    """This class is responsible for registering handlers for buttons"""
    menu: Menu

    def __init__(self):
        self.menu = Menu()

    async def admin_panel(self, message: types.Message):
        """This method is called when the admin button is pressed"""
        await message.answer(reply_markup=admin, text='admin panel')
        pass

    async def schedule(self, message: types.Message):
        """This method is called when the schedule button is pressed"""
        await message.answer('з 08:00 до 17:00')

    async def start(self, message: types.Message):
        """This method/handler is called when user is
        entering command that bot doesn't have.
        This method/handler should be registered last."""
        await message.answer('Виберіть потрібний розділ нижче👇',
                             reply_markup=start)
