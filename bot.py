from aiogram import Bot, Dispatcher
from datetime import datetime
from aiogram.filters import Command, Text
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from config import load_config

registration: dict = {(2023, 8, 2): 'Олимпиада Систематика',
                      (2023, 8, 4): 'Олимпиада по биоллогии'
                      }

starts: dict = {(2023, 8, 3): 'Олимпиада Систематика',
                (2023, 8, 5): 'Олимпиада по биоллогии'
                }
ru_months = {1: 'января',
                   2: 'февраля',
                   3: 'марта',
                   4: 'апреля',
                   5: 'мая',
                   6: 'июня',
                   7: 'июля',
                   8: 'августа',
                   9: 'сентября',
                   10: 'октября',
                   11: 'ноября',
                   12: 'декабря'}

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

button_1: KeyboardButton = KeyboardButton(text='Старт регистраций')
button_2: KeyboardButton = KeyboardButton(text='Старт олимпиад')
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
                                                        resize_keyboard=True)



@dp.message(Command(commands=['start']))
async def command_start(message: Message):
    await message.answer(text='Расписание ближайших олимпиад', reply_markup=keyboard)
#        await create_profile(user_id=message.from_user.id, state='not_ignore')

@dp.message(Text(text='Старт регистраций'))
async def send_registration(message: Message):
    await message.answer(text=f'На следующей неделе начинается регистрация на: \n{olympic_reg}')  # ,reply_markup=ReplyKeyboardRemove())

@dp.message(Text(text='Старт олимпиад'))
async def send_start(message: Message):
    await message.answer(text=f'На следующей неделе начинаются олимпиады: \n{olympic_start}')  # ,reply_markup=ReplyKeyboardRemove())



if __name__ == '__main__':
    dp.run_polling(bot)