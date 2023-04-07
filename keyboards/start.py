from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Панель адміна'))\
    .row(KeyboardButton('Інше'))\
    .row(KeyboardButton('Графік роботи'), KeyboardButton('Меню'))
