from database.database import database, get_lang
from helpers.filter import Is_admin
from aiogram import types
from keyboards import user_kb
from main import dp
from main import bot
from lang import lang
from aiogram.dispatcher.filters import Text

print("Admin is connected!")

            

@dp.message_handler( Is_admin(), Text(equals=lang.gal( "chooseUser" )) )
async def choose_user(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    admin_id = message.from_user.id
    query = "SELECT * FROM conversation WHERE admin_id = %s"
    v = (admin_id, )
    ans = database.select(query, v)
    if ans == []:
        u_query = "SELECT user_id, user_name FROM user_messages"
        ans2 = database.select(u_query)
        if ans2 == []:
            await bot.send_message(message.from_user.id, lang.no_hang)
        else:
            mymark = types.InlineKeyboardMarkup()
            for a in ans2:
                mymark.insert( types.InlineKeyboardButton( a[1], callback_data="chu_" + str(a[0]) ) )
            await bot.send_message(message.from_user.id, lang.choose_user, reply_markup=mymark)
    else: 
        await bot.send_message(message.from_user.id, lang.already_have + "\nid:" + str(ans[0][1]) + "\n" + lang.name + str(ans[0][3]) + lang.please_close)

            

@dp.message_handler( Is_admin(), Text(equals=lang.gal( "closeCon" )) )
async def close_con(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    quer = "SELECT * FROM conversation WHERE admin_id = %s"
    val = (message.from_user.id, )
    ans = database.select_one(quer, val)
    if ans == {}:
        await bot.send_message(message.from_user.id, lang.no_con)
    else:
        quer = "INSERT INTO finished (id, admin_id, user_id, admin_name, user_name, rate, message, chat_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        v = (ans["ticket"], ans["admin_id"], ans["user_id"], ans["admin_name"], ans["user_name"], 0, "no rate", message.chat.id)
        an = database.insert(quer, v)
        if an == 0:
            await bot.send_message(message.from_user.id, lang.error + " #42")
        else:
            quer = "DELETE FROM conversation WHERE admin_id = %s"
            ans2 = database.insert(quer, val)
            if ans2 == 0:
                await bot.send_message(message.from_user.id, lang.error + " #43")
            else:
                lang2 = get_lang(ans["user_id"])
                await bot.send_message(message.from_user.id, lang.closed_con)
                msg = await bot.send_message(ans["user_id"], lang2.admin_closed + "\n" + lang2.please_rate, reply_markup=user_kb.rate_kb(lang2, str(ans["ticket"])))
                quer = "UPDATE finished SET message_id = %s WHERE id = %s"
                val = (msg.message_id, ans["ticket"])
                ans3= database.insert(quer, val)
                if ans3 == 0:
                    await bot.send_message(message.from_user.id, lang.error + " #40")
    

@dp.message_handler( Text(equals=lang.gal("ch_lang")) )
async def minus_handler(message: types.Message):
    lan = get_lang(message.from_user.id, message.from_user.language_code)
    b1 = [  [
                types.InlineKeyboardButton("🇺🇿 O'zbekcha 🇺🇿", callback_data="chl_uz"),
                types.InlineKeyboardButton("🇺🇿 Ўзбекча 🇺🇿", callback_data="chl_oz"),
            ],
            [
                types.InlineKeyboardButton("🇷🇺 Русский 🇷🇺", callback_data="chl_ru"),
                types.InlineKeyboardButton("🇬🇧 English 🇬🇧", callback_data="chl_en")
            ]
        ]
    km = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=b1)
    await message.answer(lan.choose_lan, reply_markup=km)

@dp.message_handler( Is_admin(), Text(equals=lang.gal( "exit" )))
async def del_myself(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    quer = "SELECT * FROM conversation WHERE admin_id = %s"
    val = (message.from_user.id, )
    ans = database.select(quer, val)
    if ans != []:
        await message.answer(lang.had_con + str(ans[0][3]) + " id: " + str(ans[0][1]) + "\n" + lang.send_wait)
        quer4 = "DELETE FROM conversation WHERE admin_id = %s"
        val4 = (message.from_user.id, )
        ans4 = database.insert(quer4, val4)
        if ans4 == 0:
            await message.answer(lang.cant_del_con)
        else:
            await message.answer(lang.con_del)
        qu = "INSERT INTO user_messages (user_id, chat_id, message, user_name) VALUES (%s, %s, %s, %s)"
        va = (ans[0][1], ans[0][1], lang.prev_admin, ans[0][3])
        ans3 = database.insert(qu, va)
        if ans3 != 0:
            lang2 = get_lang(ans[0][1])
            await bot.send_message(ans[0][1], lang2.was_deleted)
        else:
            await message.answer(lang.con_lost)
    quer2 = "DELETE FROM admins WHERE admin_id = %s"

    val2 = (message.from_user.id, )
    ans2 = database.insert(quer2, val2)
    if ans2 == 0:
        await message.answer(lang.cant_del_adm)
    else:
        await message.answer(lang.adm_del)
    await message.answer(lang.done, reply_markup=user_kb.kb_maker(lang))

