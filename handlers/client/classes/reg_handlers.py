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
    
    buttons: ButtonsHandlers
    dp: Dispatcher
    methods: list

    def __init__(self, dp: Dispatcher):
        self.buttons = ButtonsHandlers()
        self.dp = dp
        self.reg_all()

    def reg_all(self):
        """This method calls all methods of the class except itself,
        and methods that start with '__'"""

        self.methods = [
            method for method in dir(self) if callable(getattr(self, method))
            and not method.startswith("__")]

        for method in self.methods:
            if method == inspect.currentframe().f_code.co_name:
                pass
            else:
                getattr(self, method)()
        self.dp.register_message_handler(self.buttons.start)

    def buttons_func(self):
        self.dp.register_message_handler(self.buttons.admin_panel,
                                         Text(equals='Панель адміна'))
        self.dp.register_message_handler(self.buttons.schedule,
                                         Text(equals='Графік роботи'))
        self.dp.register_message_handler(self.buttons.menu.main,
                                         Text(equals=self.buttons.menu.button_name))
        self.dp.register_message_handler(self.buttons.menu.filters.main,
                                         Text(equals=self.buttons.menu.filters.button_name))
        self.dp.register_message_handler(self.buttons.menu.filters.names.add_name,
                                         Text(equals=self.buttons.menu.filters.names.button_name))
        self.dp.register_callback_query_handler(
            self.buttons.menu.back, text='back')
        self.dp.register_callback_query_handler(
            self.buttons.menu.pages, text='page')
        self.dp.register_callback_query_handler(
            self.buttons.menu.next, text='next')
