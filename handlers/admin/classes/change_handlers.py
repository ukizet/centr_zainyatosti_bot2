from aiogram import types
from aiogram.dispatcher import FSMContext
from create import db
from keyboards import cancel_button, start

from .states import Change


class ChangeHandlers:
    """Class for change data in db"""
    async def id(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['id'] = int(message.text)
        await Change.choice.set()
        await message.answer('''Введіть\n1 - якщо хочете змінити статус вакансії,\n2 - якщо хочете змінити назву вакансії\n3 - якщо хочете змінити опис вакансії,\n4 - якщо хочете змінити ЗП\n5 - якщо хочете змінити все''',
                             reply_markup=cancel_button)

    async def choice(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            try:
                data['choice'] = int(message.text)
            except:
                await message.answer('Було введено не число. Введіть число')
                return
        if data['choice'] == 1:
            await Change.status.set()
            await message.answer('Введіть новий статус вакансії',
                                 reply_markup=cancel_button)
        elif data['choice'] == 2:
            await Change.name.set()
            await message.answer('Введіть нову назву вакансії',
                                 reply_markup=cancel_button)
        elif data['choice'] == 3:
            await Change.desc.set()
            await message.answer('Введіть новий опис вакансії',
                                 reply_markup=cancel_button)
        elif data['choice'] == 4:
            await Change.salary.set()
            await message.answer('Введіть нову ЗП', reply_markup=cancel_button)
        elif data['choice'] == 5:
            await Change.status.set()
            await message.answer('Введіть новий статус вакансії',
                                 reply_markup=cancel_button)
        else:
            await message.answer('Введено не коректне число',
                                 reply_markup=start)
            await state.finish()

    async def status(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['status'] = message.text
        if data['choice'] == 5:
            await Change.name.set()
            await message.answer('Введіть нову назву вакансії',
                                 reply_markup=cancel_button)
        else:
            # await db.sql_change(message=message, state=state)
            await db.db_obj.update_data(message, 'vacancies',
                                        f"status='{data['status']}'",
                                        f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=start)

    async def name(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        if data['choice'] == 5:
            await Change.desc.set()
            await message.answer('Введіть новий опис вакансії',
                                 reply_markup=cancel_button)
        else:
            await db.db_obj.update_data(message, 'vacancies',
                                        f"name='{data['name']}'",
                                        f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=start)

    async def desc(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['desc'] = message.text
        if data['choice'] == 5:
            await Change.salary.set()
            await message.answer('Введіть нову ЗП', reply_markup=cancel_button)
        else:
            await db.db_obj.update_data(message, 'vacancies',
                                        f"desc='{data['desc']}'",
                                        f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=start)

    async def salary(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['salary'] = message.text
        if data['choice'] == 5:
            await db.db_obj.update_data(message, 'vacancies',
                                        f"status='{data['status']}', name='{data['name']}', desc='{data['desc']}',salary='{data['salary']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=start)
        else:
            await db.db_obj.update_data(message, 'vacancies',
                                        f"salary='{data['salary']}'", f"id={data['id']}")
            await state.finish()
            await message.answer('Вакансія була змінена', reply_markup=start)
