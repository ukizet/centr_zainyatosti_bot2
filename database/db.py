"""Db module for work with database"""
import os
import sqlite3 as sq
from dataclasses import dataclass

from aiogram import types
from keyboards import start


@dataclass
class Database:
    """Class for work with database"""

    current_dir: str
    conn: sq.Connection
    cursor: sq.Cursor

    def __init__(self, db_name: str):
        """
        :db_name: назва бази даних з крапкою, як тут 'database.db'
        """
        self.current_dir = os.getcwd()
        # перевірка в якій директорії запущений бот
        if self.current_dir.endswith('centr_zainyatosti_bot2'):
            self.conn = sq.connect(f'database/{db_name}')
        else:
            self.conn = sq.connect(
                f'centr_zainyatosti_bot2/database/{db_name}')
        self.cursor = self.conn.cursor()
        self.create_table(
            'vacancies',
            'ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status TEXT DEFAULT "active", name TEXT, desc TEXT, salary REAL')
        if self.conn:
            print('Database connected(class Database)')

    def create_table(self, table_name: str, columns: str):
        """
        :param table_name: назва таблиці
        :param columns: назви стовпців приблизно такого формату: 'ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status TEXT DEFAULT "active", name TEXT, desc TEXT, salary REAL'
        """

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при створенні таблиці: {e}')

    async def insert_data(self, message: types.Message, table_name: str,
                          columns: str, data: str):
        """
        :param table_name: назва таблиці
        :param columns: назви стовпців приблизно такого формату: 'name, desc, salary'
        :param data: данні які треба вставити приблизно такого формату: '"Вакансія 1", "Опис вакансії 1", 1000'
        """

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({data})"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при вставці даних: {e}')
            await message.answer(f'Помилка при вставці даних: {e}',
                                 reply_markup=start)

    async def select_data(self, message: types.Message, columns: str,
                          table_name: str, condition: str = None) -> list:
        """
        Цей метод повертає список списків, де кожен список це рядок з таблиці

        :param table_name: назва таблиці
        :param columns: назви стовпців приблизно такого формату: 'name, desc, salary'
        :param condition: умова вибору даних приблизно такого формату: 'salary > 1000'
        """

        if columns is None:
            columns = '*'
        query = f"SELECT {columns} FROM {table_name}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f'Помилка при виборці даних: {e}')
            await message.answer(f'Помилка при виборці даних: {e}',
                                 reply_markup=start)

    async def update_data(self, message: types.Message, table_name: str,
                          set_values: str, condition: str = None):
        """
        :param table_name: назва таблиці
        :param set_values: данні які треба вставити приблизно такого формату: 'name = "Вакансія 1", desc = "Опис вакансії 1", salary = 1000'
        :param condition: умова вибору даних приблизно такого формату: 'salary > 1000'
        """

        query = f"UPDATE {table_name} SET {set_values}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при оновленні даних: {e}')
            await message.answer(f'Помилка при оновленні даних: {e}', reply_markup=start)

    async def delete_data(self, message: types.Message, table_name: str,
                          condition: str = None):
        """
        :param table_name: назва таблиці
        :param condition: умова вибору даних приблизно такого формату: 'salary > 1000' або 'id = 1'
        """

        query = f"DELETE FROM {table_name}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f'Помилка при видаленні даних: {e}')
            await message.answer(f'Помилка при видаленні даних: {e}',
                                 reply_markup=start)

    def close_connection(self):
        self.conn.close()
