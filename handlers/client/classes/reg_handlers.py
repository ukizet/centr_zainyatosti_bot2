import inspect
from dataclasses import dataclass

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from buttons_handlers import ButtonsHandlers


@dataclass
class RegHandlers:
    """
    Клас для реєстрації хендлерів.
    Одразу після створення об'єкта класу,
    викликається метод reg_all, який реєструє всі хендлери.
    """
    dp: Dispatcher

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.reg_all()

    def reg_all(self):
        """This method calls all methods of the class except itself,
        and methods that start with '__'"""
        methods = [method for method in
                   dir(self.__class__.__name__) if
                   callable(getattr(self.__class__.__name__, method)) and not
                   method.startswith("__")]
        for method in methods:
            if method != inspect.currentframe().f_code.co_name:
                getattr(self, method)()

    def buttons(self):
        buttons = ButtonsHandlers()
        self.dp.register_message_handler(buttons.admin_panel,
                                         Text(equals='Панель адміна'))
        self.dp.register_message_handler(buttons.schedule,
                                         Text(equals='Графік роботи'))
        self.dp.register_message_handler(buttons.menu,
                                         Text(equals='Меню'))
