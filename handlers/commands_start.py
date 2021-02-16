from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_user

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Регистрация успешна\n'
                                            'Ожидай начала квеста😉')
    reg_user(message.chat.id)
