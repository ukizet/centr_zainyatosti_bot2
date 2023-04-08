from aiogram import types

from dataclasses import dataclass

from keyboards import admin
# from command_menu_handlers import CommandMenuHandlers
from menu_handlers import MenuHandlers


@dataclass
class ButtonsHandlers:
    """This class is responsible for registering handlers for buttons"""
    menu: MenuHandlers

    def __init__(self):
        self.menu = MenuHandlers()

    async def admin_panel(self, message: types.Message):
        """This method is called when the admin button is pressed"""
        await message.answer(reply_markup=admin, text='admin panel')
        pass

    async def schedule(self, message: types.Message):
        """This method is called when the schedule button is pressed"""
        await message.answer('з 08:00 до 17:00')
