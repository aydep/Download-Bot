from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_res360 = KeyboardButton('360p')
btn_res720 = KeyboardButton('720p')

kb_res_all = ReplyKeyboardMarkup(resize_keyboard=True)
kb_res_l = ReplyKeyboardMarkup(resize_keyboard=True)
kb_res_h = ReplyKeyboardMarkup(resize_keyboard=True)
kb_res_all.row(btn_res360, btn_res720)
kb_res_l.row(btn_res360)
kb_res_h.row(btn_res720)
