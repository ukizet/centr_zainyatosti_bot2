import inspect
from dataclasses import dataclass

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from .add_handlers import AddHandlers
from .buttons_handlers import ButtonsHandlers
from .change_handlers import ChangeHandlers
from .delete_handlers import DeleteHandlers
from .search_handlers import SearchHandlers
from .states import Add, Change, Delete, Search


@dataclass
class RegHandlers:
    """
    Клас для реєстрації хендлерів.
    Одразу після створення об'єкта класу,
    викликається метод reg_all, який реєструє всі хендлери.
    """
    dp: Dispatcher
    methods: list

    def __init__(self, dp: Dispatcher):
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

    def buttons(self):
        """This method registers handlers for buttons in start keyboard"""
        button = ButtonsHandlers()
        self.dp.register_message_handler(
            button.cancel, Text(equals='Відміна'), state="*")

        self.dp.register_message_handler(
            button.add, Text(equals='Додати вакансію'), state=None)
        self.dp.register_message_handler(
            button.change, Text(equals='Змінити вакансію'))
        self.dp.register_message_handler(
            button.delete, Text(equals='Видалити вакансію'))
        self.dp.register_message_handler(
            button.show, Text(equals='Показати вакансії'))
        self.dp.register_message_handler(
            button.search, Text(equals='Пошук вакансій'))

    def add(self):
        add_obj = AddHandlers()
        self.dp.register_message_handler(
            add_obj.name, state=Add.name)
        self.dp.register_message_handler(
            add_obj.desc, state=Add.desc)
        self.dp.register_message_handler(
            add_obj.salary, state=Add.salary)

    def delete(self):
        delete = DeleteHandlers()
        self.dp.register_message_handler(delete.del_vacancy, state=Delete.id)

    def change(self):
        change = ChangeHandlers()
        self.dp.register_message_handler(
            change.id, state=Change.id)
        self.dp.register_message_handler(
            change.choice, state=Change.choice)
        self.dp.register_message_handler(
            change.status, state=Change.status)
        self.dp.register_message_handler(
            change.name, state=Change.name)
        self.dp.register_message_handler(
            change.desc, state=Change.desc)
        self.dp.register_message_handler(
            change.salary, state=Change.salary)

    def search(self):
        search = SearchHandlers()
        self.dp.register_message_handler(
            search.name, state=Search.name)
