from aiogram import types
from aiogram.dispatcher import FSMContext
from classes.states import Add, Change, Delete, Search
from keyboards import cancel_button, start
from create import db


class ButtonsHandlers:
    """Клас для обробки кнопок клавіатури адміністратора"""
    async def add(self, message: types.Message):
        """Додавання нової вакансії"""
        await Add.name.set()
        await message.answer('Пишіть назву вакансії',
                             reply_markup=cancel_button)

    async def change(self, message: types.Message):
        """Зміна вакансії"""
        await message.answer('Ще в розробці', reply_markup=start)
        await Change.id.set()
        await message.answer('Введіть id вакансії яку треба змінити',
                             reply_markup=cancel_button)

    async def delete(self, message: types.Message):
        """Видалення вакансії"""
        # await message.answer('Ще в розробці', reply_markup=client)
        await Delete.id.set()
        # await DeleteVacancy.condition.set()
        await message.answer('Введіть id вакансії яку треба видалити',
                             reply_markup=cancel_button)

    async def show(self, message: types.Message):
        """Виведення всіх вакансій"""
        # await db.sql_read_admin(message=message)
        for vacancy in await db.select_data(message, '*', 'vacancies'):
            await message.answer(f'ID: {vacancy[0]}\nСтатус: {vacancy[1]}\nНазва вакансії: {vacancy[2]}\nОпис: {vacancy[3]}\nЗП: {vacancy[4]}')

    async def cancel(self, message: types.Message, state: FSMContext):
        """Скасування операції"""
        current_state = await state.get_state()
        print(f'current_state: {current_state}')
        if current_state is None:
            # print(f'current_state: IS NONE!!!')
            return
        await state.finish()
        await message.answer('Операція була скасована',
                             reply_markup=start)

    async def search(self, message: types.Message):
        """Пошук вакансії"""
        # await message.answer('Ще в розробці', reply_markup=start)
        await Search.name.set()
        await message.answer('Введіть назву вакансії яку треба знайти',
                             reply_markup=cancel_button)
