from dataclasses import dataclass

from aiogram.types import (
    ReplyKeyboardMarkup
)


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
