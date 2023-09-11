from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = [
        [
            KeyboardButton(text="Сам/Сама🙋‍♂️"),
            KeyboardButton(text="Сімейна пара👫"),
        ],
        [
            KeyboardButton(text="Група людей👨‍👨‍👦‍👦")
        ]
    ]
keyboard_find = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=False)

kb_choose = [
    [
        KeyboardButton(text="Так"),
        KeyboardButton(text="Ні"),

    ],
]
keyboard_choose = ReplyKeyboardMarkup(keyboard=kb_choose)


builder = InlineKeyboardBuilder()
builder.add(InlineKeyboardButton(text="Ім'я🙋‍♂️", callback_data='name_update'))
builder.add(InlineKeyboardButton(text="Телефон📞", callback_data='phone_update'))
builder.add(InlineKeyboardButton(text="Для кого шукаєте роботу🔎", callback_data='job_search_target_update'))
builder.adjust(2, 2)