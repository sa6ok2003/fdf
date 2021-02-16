from aiogram import types
from misc import dp, bot
import sqlite3
from aiogram.dispatcher import FSMContext
from .sqlit import stata_user
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 941730379 #Бекир

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3]

class reg(StatesGroup):
    name = State()
    fname = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        await bot.send_message(message.chat.id, 'Привет админ!')
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        markup.add(bat_a, bat_b)
        await bot.send_message(message.chat.id,'Выбери что хочешь сделать:',reply_markup=markup)


@dp.callback_query_handler(text='list_members')
async def admin_1(call: types.callback_query):
    status = stata_user()
    await bot.send_message(call.message.chat.id, f'Всего пользователей: {status}')



@dp.callback_query_handler(text='write_message')
async def rassilka (call:types.callback_query,state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА',callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id,'Перешли мне уже готовый пост и я разошлю его всем юзерам',reply_markup=murkap)
    await reg.name.set()


@dp.message_handler(state=reg.name,content_types=['text','photo','video','video_note'])
async def fname_step(message: types.Message, state: FSMContext):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    for i in sql.execute("SELECT id FROM user_time"):
        await message.copy_to(i[0])
    await state.finish()
    await bot.send_message(message.chat.id, 'Рассылка выполенена!')