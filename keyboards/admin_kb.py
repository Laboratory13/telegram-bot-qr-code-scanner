from aiogram import types
from lang import lang

def kb_maker(lang:lang.en):
    bu = types.KeyboardButton(lang.chooseUser)
    bv = types.KeyboardButton(lang.closeCon)
    bu1 = types.KeyboardButton(lang.ch_lang)
    bu2 = types.KeyboardButton(lang.exit)
    return types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).insert(bu).insert(bv).insert(bu1).insert(bu2)

def super_kb(lang:lang.en):
    bu = types.KeyboardButton(lang.chooseUser)
    bv = types.KeyboardButton(lang.closeCon)
    bu1 = types.KeyboardButton(lang.ch_lang)
    bu2 = types.KeyboardButton(lang.exit)
    bu3 = types.KeyboardButton(lang.allAdmins)
    bu4 = types.KeyboardButton(lang.delAdmin)
    return types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).insert(bu).insert(bv).insert(bu1).insert(bu2).insert(bu3).insert(bu4)