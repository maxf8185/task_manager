from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

keyboard = ReplyKeyboardBuilder()
keyboard.add(
    types.KeyboardButton(text='options'),
    types.KeyboardButton(text='schedule'),
    types.KeyboardButton(text='links'),
    types.KeyboardButton(text='homeworks'),
    types.KeyboardButton(text='about'),
)
keyboard.adjust(3, 2)

films_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='view all films'),
        ],
        [
            types.KeyboardButton(text='add new film'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your option'
)