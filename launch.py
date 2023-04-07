from aiogram import executor

from create import dp


async def on_startup(dispatcher):
    print('Bot is online')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
