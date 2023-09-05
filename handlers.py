from typing import Dict, Any

import gspread_asyncio
import pandas as pd
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, Message, CallbackQuery
import logging
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters import Command, CommandStart
from states import Info
from google.oauth2.service_account import Credentials


router = Router()


def get_creds():
    creds = Credentials.from_service_account_file("api_data.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


@router.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):

    kb = [
        [
            KeyboardButton(text="Tak"),
            KeyboardButton(text="Нi")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await state.update_data(name=message.from_user.full_name)
    await state.set_state(Info.is_looking)
    await message.answer(f"Привiт {message.from_user.full_name} !\n Я бот вiд СelPlus!\nШукаэш роботу?.",
                        reply_markup=keyboard)




@router.message(Info.is_looking, F.text == 'Tak')
async def show_jobs(message: Message, state: FSMContext):
    client = await agcm.authorize()

    await state.update_data(is_looking=message.text)
    spread = await client.open('test_spreadsheet')
    worksheet = await spread.worksheet('Sheet1')
    records = await worksheet.get_all_records()
    builder = InlineKeyboardBuilder()
    for record in records:
        builder.add(InlineKeyboardButton(text=record['zawód'], callback_data='job ' + record['zawód']))

    builder.adjust(2)

    text = f'Здаров {message.from_user.first_name}, э така роботка: \n'
    for item in records:
        text += f'{item["zawód"]} - {item["opis"]} - {item["ilość miejsc"]} \n'
    text += 'ну як?'

    await message.answer("Виберіть роботу: ", reply_markup=ReplyKeyboardRemove())
    await message.answer(text, reply_markup=builder.as_markup())


@router.message(Info.is_looking, F.text == 'Нi')
async def process_no(message: Message, state: FSMContext):
    await state.update_data(is_looking=message.text)
    await show_summary(message, await state.get_data(), positive=False)


@router.callback_query(F.data.startswith('job '))
async def show_job(query: CallbackQuery, state: FSMContext):
    print(query.data)
    await state.update_data(job=query.data[4:])
    await query.message.answer('Вибрано роботу ' + query.data[4:])
    await state.set_state(Info.phone_number)
    await query.message.answer('Введіть номер телефону: ')


@router.message(Info.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await show_summary(message, await state.get_data(), positive=True)





@router.message(Command('cancel'))
@router.message(F.text.casefold() == 'cancel')
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.clear()
    await message.answer("Ви скасували реєстрацію", reply_markup=ReplyKeyboardRemove())


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True):
    name = data['name']
    job =  data['job'] if 'job' in data else 'не вибрано'
    phone_number = data['phone_number'] if 'phone_number' in data else 'не вказано'
    text = f"Ваша інформація:\n Ім'я: {name} Телефон: {phone_number} \nДякуэмо за реэстрацію!  \n"
    text += (f"Ми вам зателефонуэмо! за справою працi {job}" if positive else "Ви не шукаэте роботу")
    client = await agcm.authorize()

    if positive:
        df = pd.DataFrame({'imię nazwisko': [name], 'zawód': [job]})
        df_values = df.values.tolist()
        print(df_values)
        spread = await client.open('test_spreadsheet')
        sheet = await spread.worksheet('Sheet2')
        await sheet.append_row([name, job, phone_number], value_input_option='RAW')
        print(sheet)

    await message.answer(text, reply_markup=ReplyKeyboardRemove())