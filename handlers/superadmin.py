from database.database import database, get_lang
from helpers.filter import  Is_super_admin
from aiogram import types
from main import dp
from main import bot
from lang import lang
from aiogram.dispatcher.filters import Text


@dp.message_handler( Is_super_admin(), Text(equals=lang.gal( "delAdmin" )))
async def del_admin(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    adm = "SELECT admin_id, admin_name, avg_rate, super FROM admins"
    ans = database.select(adm)
    if ans != []:
        mymark = types.InlineKeyboardMarkup()
        for a in ans:
            text = str(a[1]) + " " + str(a[2])
            text = "⭐️" + text if a[3] == 1 else "👤" + text
            mymark.insert(types.InlineKeyboardButton(text, callback_data="del_" + str(a[0])))
        await bot.send_message(message.from_user.id, text=lang.del_admin, reply_markup=mymark)

@dp.message_handler( Is_super_admin(), Text(equals=lang.gal( "allAdmins" )))
async def show_admins(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    adm = "SELECT admin_id, admin_name, start_date, con_count, avg_rate, super FROM admins"
    ans = database.select(adm)
    if ans != []:
        text = "🆔" + lang.user_id + "\t\t\t⭐️" + lang.spr + "\t\t\t" + lang.name + "\t\t\t" + lang.chats + "\t\t\t📈" + lang.rate + "\t\t\t" + "\n"
        for ad in ans:
            is_super = "⭐️" if ad[5] == 1 else "👤"
            text = text + "🆔" + str(ad[0]) + "\t\t\t" + is_super + str(ad[1]) + "\t\t\t⚔️" + str(ad[3]) + "\t\t\t📈" + str(round(ad[4],2)) + "\n"
        await message.answer(text)
    else:
        await message.answer(lang.error + "#73")