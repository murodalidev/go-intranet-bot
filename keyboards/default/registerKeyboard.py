from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

registerKey = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Ro'yhatdan o'tish"),
            KeyboardButton(text="📜 Qo'llanma"),
        ]
    ],
    resize_keyboard=True
)


sendPhoneKey = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📲 Telefon raqamini jo'natish", request_contact=True)]
    ],
    resize_keyboard=True
)

confirmKey = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Tasdiqlayman")],
        [KeyboardButton(text="❌ Boshidan boshlash")],
    ],
    resize_keyboard=True
)
