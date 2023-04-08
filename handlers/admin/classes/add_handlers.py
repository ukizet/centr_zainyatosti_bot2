"""Handlers for add states"""
from aiogram import types
from aiogram.dispatcher import FSMContext

from create import db
from keyboards import start

from .states import Add


class AddHandlers:
    """Class for add handlers"""
    async def load_template(self, message: types.Message, state: FSMContext,
                            load_type: str, text: str = '',
                            finish: bool = False, test: bool = False):
        """Template for load data to db"""
        async with state.proxy() as data:
            data[f'{load_type}'] = message.text
        if finish is True:
            async with state.proxy() as data:
                await message.answer(str(data), reply_markup=start)
            # await db.sql_add(state=state)
            async with state.proxy() as data:
                await db.insert_data(message, 'vacancies',
                                            'name, desc, salary',
                                            f"'{data['name']}', '{data['desc']}', '{data['salary']}'")
            await state.finish()
        else:
            await Add.next()
            if len(text) > 0:
                await message.answer(f'{text}')
            else:
                pass

    async def name(self, message: types.Message, state: FSMContext):
        """Handler for add name state"""
        await self.load_template(message=message, state=state,
                                 load_type='name', text='Пишіть опис вакансії')

    async def desc(self, message: types.Message, state: FSMContext):
        """Handler for add desc state"""
        await self.load_template(message=message, state=state,
                                 load_type='desc', text='Пишіть ЗП')

    async def salary(self, message: types.Message, state: FSMContext):
        """Handler for add salary state"""
        await self.load_template(message=message, state=state,
                                 load_type='salary', text='', finish=True)
