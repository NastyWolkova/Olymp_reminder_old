from aiogram import Bot, Dispatcher
from datetime import datetime
from aiogram.filters import Command, Text
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import load_config
import sqlite3 as sq
from texts import registration, starts, ru_months


def close_events(my_dict):
    result: dict = {}
    new_key: str
    for key in my_dict:
        delta = datetime(*key) - datetime.now()
        if delta.days <= 7:
            new_key = f'{key[2]} {ru_months[key[1]]}'
            result[new_key] = my_dict[key]
    return result

olympic_reg = close_events(registration)
olympic_start = close_events(starts)

# def create_profile(user_id, state):
# #    global db, cursor
#     with sq.connect('olympic_bot/ids.db') as db:
#         cursor = db.cursor()
#     #user = cur.execute(f'SELECT 1 FROM ids WHERE user_id == "{user_id}"').fetchone()
#     #if not user:
#         cursor.execute('INSERT INTO ids VALUES(?,?)', (user_id, state))


config = load_config('.env')
superadmin = config.tg_bot.admin_ids[0]

bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()
kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

button_1: KeyboardButton = KeyboardButton(text='Старт регистраций')
button_2: KeyboardButton = KeyboardButton(text='Старт олимпиад')
button_3: KeyboardButton = KeyboardButton(text='Напомнить/отказаться')
#keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
#                                                        resize_keyboard=True)
kb_builder.row(button_1, button_2, width=2)
kb_builder.row(button_3, width=1)


def db_table_val(user_id: int, state: str):
    conn = sq.connect('db.db', check_same_thread=False)
    cursor = conn.cursor()
    user = cursor.execute(f'SELECT 1 FROM users WHERE user_id == "{user_id}"').fetchone()
    if not user:
        cursor.execute('INSERT INTO users (user_id, state) VALUES (?, ?)', (user_id, state))
    conn.commit()
    conn.close()

def db_change_state(user_id: int):
    conn = sq.connect('db.db', check_same_thread=False)
    cursor = conn.cursor()
    state = cursor.execute(f'SELECT state FROM users WHERE user_id == "{user_id}"').fetchall()
    if state[0][0] == 'not_ignore':
        #change to 'ignore'
        cursor.execute(f'UPDATE users SET state = "ignore" WHERE user_id == "{user_id}"')
        text = 'Вы отказались от уведомлений.'
    else:
        #change to 'not_ignore'
        cursor.execute(f'UPDATE users SET state = "not_ignore" WHERE user_id == "{user_id}"')
        text = 'Вы согласились на уведомления.'
    conn.commit()
    conn.close()
    return text


@dp.message(Command(commands=['start']))
async def command_start(message: Message):
    db_table_val(user_id=message.from_user.id, state='not_ignore')
    await message.answer(text='Расписание ближайших олимпиад', reply_markup=kb_builder.as_markup(resize_keyboard=True))
#        await create_profile(user_id=message.from_user.id, state='not_ignore')

@dp.message(Text(text='Старт регистраций'))
async def send_registration(message: Message):
    await message.answer(text=f'На следующей неделе начинается регистрация на: \n{olympic_reg}')  # ,reply_markup=ReplyKeyboardRemove())

@dp.message(Text(text='Старт олимпиад'))
async def send_start(message: Message):
    await message.answer(text=f'На следующей неделе начинаются олимпиады: \n{olympic_start}')

@dp.message(Text(text='Напомнить/отказаться'))
async def send_start(message: Message):
    await message.answer(text=f'{db_change_state(message.from_user.id)}')


if __name__ == '__main__':
    dp.run_polling(bot)