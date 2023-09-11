from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove,Message, CallbackQuery
import logging

from aiogram.filters import Command, CommandStart

from buttons import keyboard_find, keyboard_choose, builder
from helpers import  validate_phone_number
from request import add_lead
from states import Info


router = Router()


@router.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    await state.set_state(Info.job_search_target)
    await message.answer("👋Вас вітає бот кадрової агенції <b>Cel Plus</b>🎯  \nТут Ви можете залишити свою заявку, щоб наші"
                         " рекрутери зв'язалися з Вами і допомогли знайти <b>роботу в Польщі</b>🇵🇱")
    await message.answer('🔎Для кого Ви шукаєте роботу?', reply_markup=keyboard_find)


@router.message(Info.job_search_target)
async def process_job_search_target(message: Message, state: FSMContext):
    await state.update_data(job_search_target=message.text)
    await message.answer("🙋‍♂️Як до Вас звертатись?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Info.name)


@router.message(Info.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞Вкажіть, будь ласка, Ваш контактний номер телефону з кодом країни"
                         " (+48 Польща, +380 Україна, тощо):")
    await state.set_state(Info.phone)


@router.message(Info.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = "".join(message.text.split())
    if not validate_phone_number(phone):
        return await message.answer('📞Введіть номер телефону правильно: \n \n'
                                    '<i>Правильний номер телефону повинен починатися з одного з наступних префіксів:'
                                    ' +380, 380, +48 або 48, а після префіксу має бути від 8 до 10 цифр без будь-яких'
                                    ' інших символів чи роздільників</i> ')


    await state.update_data(phone=message.text)
    await show_summary(message, state)


async def show_summary(message: Message, state: FSMContext):

    data = await state.get_data()
    await message.answer(f"ℹ️Ваші дані: \n🙋‍♂️Ім'я: <b>{data['name']}</b> \n📞Телефон: <b>{data['phone']}</b> \n"
                         f"👨‍👩‍👦‍👦Ви шукаєте роботу для: "
                         f"<b>{data['job_search_target']}</b>")
    await message.answer("<b>Все вірно?</b>", reply_markup=keyboard_choose)
    await message.answer("Якщо все вірно, натисніть <b>Так</b> ✅, якщо ні - <b>Ні</b> ❌")

    await state.set_state(Info.is_correct)


@router.message(Info.is_correct, F.text == 'Так')
async def process_is_correct(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    phone = data['phone']
    job_search_target = data['job_search_target']
    add_lead(name, phone, job_search_target)
    await message.answer("☎️<b>Дякуємо за заявку!</b> Ми зв'яжемось з Вами найближчим часом, щоб запропонувати роботу і "
                         "відповісти на всі Ваші запитання! \n<b>Бажаємо гарного дня!</b>☀️✨", reply_markup=ReplyKeyboardRemove())
    await state.clear()

# @router.message()
# async def reply_on_every_message(message: Message):
#     await message.answer('every message after ')

@router.message(Info.is_correct, F.text == 'Ні')
async def process_is_correct(message: Message, state: FSMContext):

    await message.answer("Якi данi невiрнi?", reply_markup=ReplyKeyboardRemove())
    await message.answer("Виберіть, що потрібно виправити:", reply_markup=builder.as_markup())


@router.callback_query(F.data == 'name_update')
async def process_name_update(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🙋‍♂️Введіть ім'я:")
    await state.set_state(Info.name_update)


@router.message(Info.name_update)
async def process_name_update(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await show_summary(message, state)


@router.callback_query(F.data == 'phone_update')
async def process_phone_update(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📞Введіть номер телефону:")
    await state.set_state(Info.phone_update)


@router.message(Info.phone_update)
async def process_phone_update(message: Message, state: FSMContext):
    phone = ''.join(message.text.split())
    if not validate_phone_number(phone):
        return await message.answer('📞Введіть номер телефону правильно: \n \n'
                                    '<i>Правильний номер телефону повинен починатися з одного з наступних префіксів:'
                                    ' +380, 380, +48 або 48, а після префіксу має бути від 8 до 10 цифр без будь-яких'
                                    ' інших символів чи роздільників</i> ')
    await state.update_data(phone=message.text)
    await show_summary(message, state)


@router.callback_query(F.data == 'job_search_target_update')
async def process_job_search_target_update(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🔎Для кого Ви шукаєте роботу?", reply_markup=keyboard_find)
    await state.set_state(Info.job_search_target_update)


@router.message(Info.job_search_target_update)
async def process_job_search_target_update(message: Message, state: FSMContext):
    await state.update_data(job_search_target=message.text)
    await show_summary(message, state)


@router.message(Command('cancel'))
@router.message(F.text.casefold() == 'cancel')
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.clear()
    await message.answer("Ви скасували реєстрацію", reply_markup=ReplyKeyboardRemove())
    await message.answer_sticker( sticker='CAACAgIAAxkBAAElxC5k-g3VwZUCAAFChZoAASfkM4fiw5XvAAJeAAPBnGAM2cOQTay6uFAwBA')
