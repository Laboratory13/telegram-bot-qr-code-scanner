from aiogram import types
from database.database import database, get_lang
from keyboards import user_kb
from main import dp
from main import bot
from aiogram.dispatcher.filters import Text
from helpers.filter import Is_writing
from lang import lang

print("User is connected!")


@dp.message_handler( Is_writing(), content_types = [types.ContentType.TEXT] )
async def report_handler(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    quer = "Update finished SET message = %s, writing = %s WHERE user_id = %s AND writing = %s"
    val = (message.text, 0, message.from_user.id, 1)
    ans = database.insert(quer, val)
    if ans == 0:
        await message.answer(lang.error + " #21", reply_markup=user_kb.kb_maker(lang))
    else:
        await message.answer(lang.feedback, reply_markup=user_kb.kb_maker(lang))


@dp.message_handler(Text(equals=lang.gal("close_con")))
async def close_con_user(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    quer = "SELECT * FROM conversation WHERE user_id = %s"
    val = (message.from_user.id, )
    ans = database.select_one(quer, val)
    if ans == {}:
        await bot.send_message(message.from_user.id, lang.no_con)
    else:
        quer = "INSERT INTO finished (id, admin_id, user_id, admin_name, user_name, rate, message, chat_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        v = (ans["ticket"], ans["admin_id"], ans["user_id"], ans["admin_name"], ans["user_name"], 0, "no rate", message.chat.id)
        an = database.insert(quer, v)
        if an == 0:
            await bot.send_message(message.from_user.id, lang.error + " #19")
        else:
            quer = "DELETE FROM conversation WHERE user_id = %s"
            ans2 = database.insert(quer, val)
            if ans2 == 0:
                await bot.send_message(message.from_user.id, lang.error + " #18")
            else:
                lang_2 = get_lang(ans["admin_id"])
                await bot.send_message(ans["admin_id"], lang_2.user_closed)
                msg = await bot.send_message(message.from_user.id, lang.closed_con + "\n" + lang.please_rate, reply_markup=user_kb.rate_kb(lang, str(ans["ticket"])))
                quer = "UPDATE finished SET message_id = %s WHERE id = %s"
                val = (msg.message_id, ans["ticket"])
                ans3= database.insert(quer, val)
                if ans3 == 0:
                    await bot.send_message(message.from_user.id, lang.error + " #99")