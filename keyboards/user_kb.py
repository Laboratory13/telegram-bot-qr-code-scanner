from aiogram import types
from lang import lang


# print(message.from_user.language_code)
def kb_maker( lang:lang.ru ):
    bu = types.KeyboardButton( lang.share_contact, request_contact = True )
    return types.ReplyKeyboardMarkup( resize_keyboard=True ).insert( bu )

def lang_kb() -> types.ReplyKeyboardMarkup:
    b1 = [
            [
                types.KeyboardButton("🇺🇿 O'zbekcha 🇺🇿"),
                types.KeyboardButton("🇷🇺 Русский 🇷🇺")
            ]
        ]
    return types.ReplyKeyboardMarkup( keyboard=b1, resize_keyboard=True, one_time_keyboard=True, row_width=2 )

def menu_kb( lang:lang.ru ):
    kb = [
        [
            types.KeyboardButton(lang.check),
            types.KeyboardButton(lang.settings)
        ],
        {
            types.KeyboardButton(lang.instructions),
            types.KeyboardButton(lang.contact_us)
        }
    ]
    return types.ReplyKeyboardMarkup( keyboard=kb, resize_keyboard=True, row_width=2 )

def qr_kb( lang:lang.ru, msg_id, chat_id ):
    ikb1 = types.InlineKeyboardButton( lang.accept, callback_data="qr_" + str( msg_id ) + "_" + str( chat_id ) )
    ikb2 = types.InlineKeyboardButton( lang.reject, callback_data="ro_" + str( msg_id ) + "_" + str( chat_id ) )
    return types.InlineKeyboardMarkup( row_width=2 ).insert( ikb1 ).insert( ikb2 )

def settings_kb( lang:lang.ru ) -> types.ReplyKeyboardMarkup:
    b1 = types.KeyboardButton( lang.menu )
    return lang_kb().insert( b1 )

def admin_settings_kb( lang:lang.ru ) -> types.ReplyKeyboardMarkup:
    b1 = types.KeyboardButton( lang.change_video )
    return settings_kb( lang ).insert( b1 )

def reject( lang:lang.ru ):
    b1 = types.KeyboardButton( lang.close )
    return types.ReplyKeyboardMarkup( resize_keyboard=True ).insert( b1 )