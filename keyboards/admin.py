from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Додати вакансію'), KeyboardButton('Змінити вакансію'))\
    .row(KeyboardButton('Видалити вакансію'), KeyboardButton('Показати вакансії'))\
    .row(KeyboardButton("Пошук вакансій"))\
    .row(KeyboardButton('Повернутися назад'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Відміна'))