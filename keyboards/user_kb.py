from aiogram import types
from lang import lang


# print(message.from_user.language_code)
def kb_maker(lang:lang.en):
    bu = types.KeyboardButton(lang.close_con)
    bv = types.KeyboardButton(lang.ch_lang)
    return types.ReplyKeyboardMarkup(resize_keyboard=True).insert(bu).insert(bv)

def rate_kb(lang:lang.en, c):
    b1 = [
            types.InlineKeyboardButton("1😡", callback_data="rate_1_" + c ),
            types.InlineKeyboardButton("2😭", callback_data="rate_2_" + c ),
            types.InlineKeyboardButton("3😢", callback_data="rate_3_" + c ),
            types.InlineKeyboardButton("4🙂", callback_data="rate_4_" + c ),
            types.InlineKeyboardButton("5☺️", callback_data="rate_5_" + c )
        ]
    return types.InlineKeyboardMarkup(5, [b1])

def no_kb(lang:lang.en):
    return types.ReplyKeyboardMarkup([[types.KeyboardButton(lang.tell_no)]],resize_keyboard=True)
