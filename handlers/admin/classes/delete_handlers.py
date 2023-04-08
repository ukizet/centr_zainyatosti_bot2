from aiogram import types
from aiogram.dispatcher import FSMContext

from create import db
from keyboards import start

from dataclasses import dataclass


@dataclass
class DeleteHandlers:
    """Class for delete handlers"""
    id: int

    def __init__(self):
        pass

    async def del_vacancy(self, message: types.Message, state: FSMContext):
        try:
            self.id = int(message.text)
        except Exception as e:
            await message.answer('Було введено не число. Введіть число')
            await message.answer(f'Помилка: {e}')
            return
        # await db.sql_delete(message=message)
        await db.delete_data(message, 'vacancies', f'id={id}')
        await state.finish()
        await message.answer('Вакансія була видалена', reply_markup=start)
