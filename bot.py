from aiogram import Bot, Dispatcher
from datetime import datetime
from aiogram.filters import Command, Text
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import load_config
from modules import*



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