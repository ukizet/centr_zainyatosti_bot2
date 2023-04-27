from aiogram import types
from aiogram.dispatcher import FSMContext
from create import db
from keyboards import admin


class SearchHandlers:
    """Class for search handlers"""
    async def name(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        vacancies = await db.select_data(message, '*', 'vacancies',
                                            f'name LIKE "%{data["name"]}%"')
        if len(vacancies) == 0:
            await message.answer('Вакансій з таким іменем не знайдено',
                                 reply_markup=admin)
            await state.finish()
            return
        for vacancy in vacancies:
            await message.answer(
                f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')
        await state.finish()
