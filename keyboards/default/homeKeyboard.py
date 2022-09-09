from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

homeKey = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔙 Orqaga qaytish'),
        ]
    ],
    resize_keyboard=True
)
