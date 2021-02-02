from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_res360 = KeyboardButton('360p')
btn_res720 = KeyboardButton('720p')

kb_res = ReplyKeyboardMarkup(resize_keyboard=True)
kb_res.row(btn_res360, btn_res720)
