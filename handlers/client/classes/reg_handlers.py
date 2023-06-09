import inspect
from dataclasses import dataclass

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from .buttons_handlers import ButtonsHandlers


@dataclass
class RegHandlers:
    """
    Клас для реєстрації хендлерів.
    Одразу після створення об'єкта класу,
    викликається метод reg_all, який реєструє(викликає методи) всі хендлери крім себе.
    """
    buttons_obj: ButtonsHandlers
    dp: Dispatcher
    methods: list

    def __init__(self, dp: Dispatcher):
        self.buttons_obj = ButtonsHandlers()
        self.dp = dp
        self.reg_all()

    def reg_all(self):
        """This method calls all methods of the class except itself,
        and methods that start with '__'"""

        self.methods = [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")]

        for method in self.methods:
            if method == inspect.currentframe().f_code.co_name:
                pass
            else:
                getattr(self, method)()
        self.dp.register_message_handler(self.buttons_obj.start)

    def buttons(self):
        self.dp.register_message_handler(self.buttons_obj.admin_panel,
                                         Text(equals='Панель адміна'))
        self.dp.register_message_handler(self.buttons_obj.schedule,
                                         Text(equals='Графік роботи'))
        self.dp.register_message_handler(self.buttons_obj.menu.display_menu,
                                         Text(equals='Меню'))
        self.dp.register_callback_query_handler(
            self.buttons_obj.menu.inline_button_back, text='back')
        self.dp.register_callback_query_handler(
            self.buttons_obj.menu.inline_button_next, text='next')
