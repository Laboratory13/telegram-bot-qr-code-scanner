from aiogram.dispatcher.filters import Text
from aiogram import types
from database.database import database, get_lang, get_lang_str
from datetime import datetime
from keyboards import admin_kb, user_kb
from main import dp
from main import bot
from helpers.filter import Is_admin, Is_super_admin


# callback handler for choosing user from list of hanging users
@dp.callback_query_handler(Is_admin(), Text(startswith="chu_"))
async def change_user_call(callback : types.CallbackQuery):
    lang = get_lang(callback.from_user.id, callback.from_user.language_code)
    user_id = int( callback.data.split("_")[1] )
    user = callback.from_user
    try: 
        user = await bot.get_chat(user_id)
    except:
        await callback.answer(lang.internal)
    quer = "SELECT * FROM user_messages WHERE user_id = %s"
    val = (user_id, )
    ans = database.select(quer, val)
    if ans == []:
        await callback.message.answer(lang.choose_new + " " + lang.chooseUser)
        await callback.answer()
    # ('1212', '1322131', '12312412', 'Lasiwersnf', 'Assdfhy ', '2022-09-30 07:15:07.000000', '2022-09-30 07:15:07.000000', '0', '1212313')
    else:
        query = "DELETE FROM user_messages WHERE user_id = %s"
        v = (user_id, )
        ans2 = database.insert(query, v)
        if ans2 == 0:
            await callback.message.answer(lang.choose_new + " " + lang.chooseUser)
            await callback.answer()
        else:
            lang_str = get_lang_str(callback.from_user.id, callback.from_user.language_code)
            await callback.message.answer(lang.user + str(ans[0][3]) + "\n" + lang.user_id + str(ans[0][0]) + "\n" + lang.date + str(ans[0][4]) + "\n" + lang.lang + lang_str)
            await callback.message.answer(ans[0][2])
            quer = "INSERT INTO conversation (admin_id, user_id, admin_name, user_name, start_date, last_date) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (callback.from_user.id, user_id, callback.from_user.full_name, user.full_name, datetime.now(), datetime.now())
            res = database.insert(quer, val)
            if res == 0:
                await callback.message.answer(lang.con_start_err + " " + lang.chooseUser)
                await callback.answer(lang.error)
            else:
                await callback.answer(lang.chosen)

# callback handler for deleting admins from admin list
@dp.callback_query_handler(Is_super_admin(), Text(startswith="del_"))
async def del_admin(callback : types.CallbackQuery):
    lang = get_lang(callback.from_user.id, callback.from_user.language_code)
    quer = "SELECT * FROM conversation WHERE admin_id = %s"
    del_admin_id = callback.data.split("_")[1]
    if int(del_admin_id) == callback.from_user.id:
        await callback.answer(lang.thisisyou)
    else:
        val = (del_admin_id, )
        ans = database.select(quer, val)
        if ans != []:
            await callback.message.answer(lang.had_con + str(ans[0][3]) + " id: " + str(ans[0][1]) + "\n" + lang.send_wait)
            quer4 = "DELETE FROM conversation WHERE admin_id = %s"
            val4 = (del_admin_id, )
            ans4 = database.insert(quer4, val4)
            if ans4 == 0:
                await callback.message.answer(lang.cant_del_con)
            else:
                await callback.message.answer(lang.con_del)
            qu = "INSERT INTO user_messages (user_id, chat_id, message, user_name) VALUES (%s, %s, %s, %s)"
            va = (ans[0][1], ans[0][1], lang.prev_admin, ans[0][3])
            ans3 = database.insert(qu, va)
            if ans3 != 0:
                user_lang = get_lang(ans[0][1])
                await bot.send_message(ans[0][1], user_lang.was_deleted)
            else:
                await callback.message.answer(lang.con_lost)
        quer2 = "DELETE FROM admins WHERE admin_id = %s"
        val2 = (del_admin_id, )
        ans2 = database.insert(quer2, val2)
        if ans2 == 0:
            await callback.message.answer(lang.cant_del_adm)
        else:
            await callback.message.answer(lang.adm_del)
            del_admin_lang = get_lang(del_admin_id)
            await bot.send_message(del_admin_id, del_admin_lang.admin_del_you, reply_markup=user_kb.kb_maker(del_admin_lang))
        await callback.answer(lang.done)


@dp.callback_query_handler(Is_super_admin(), Text(startswith="chl_"))
async def change_lang_adm(callback : types.CallbackQuery):
    lan = callback.data.split("_")[1]
    lang = get_lang(callback.from_user.id, lan, True)
    quer = "SELECT * FROM lang WHERE id = %s"
    val = (callback.from_user.id, )
    ans = database.select(quer, val)
    if ans == []:
        quer = "INSERT INTO lang (id, lang) VALUES (%s, %s)"
        val = (callback.from_user.id, lan)
        ans1 = database.insert(quer, val)
        if ans1 == 0:
            await callback.message.answer(lang.error + " #81")
            await callback.answer(lang.error + " #81")
        else:
            await bot.send_message(callback.from_user.id, lang.done, reply_markup=admin_kb.super_kb(lang))
            await callback.answer(lang.done)
    else:
        quer = "UPDATE lang SET lang = %s WHERE id = %s"
        val = (lan, callback.from_user.id)
        ans2 = database.insert(quer, val)
        if ans2 == 0:
            await callback.answer(lang.same_lang)
        else:
            # await callback.message.answer("Database was updated!")
            await bot.send_message(callback.from_user.id, lang.done, reply_markup=admin_kb.super_kb(lang))
            await callback.answer()

@dp.callback_query_handler(Is_admin(), Text(startswith="chl_"))
async def change_lang_adm(callback : types.CallbackQuery):
    lan = callback.data.split("_")[1]
    lang = get_lang(callback.from_user.id, lan, True)
    quer = "SELECT * FROM lang WHERE id = %s"
    val = (callback.from_user.id, )
    ans = database.select(quer, val)
    if ans == []:
        quer = "INSERT INTO lang (id, lang) VALUES (%s, %s)"
        val = (callback.from_user.id, lan)
        ans1 = database.insert(quer, val)
        if ans1 == 0:
            await callback.message.answer(lang.error + " #13")
            await callback.answer(lang.error + " #13")
        else:
            await bot.send_message(callback.from_user.id, lang.done, reply_markup=admin_kb.kb_maker(lang))
            await callback.answer(lang.done)
    else:
        quer = "UPDATE lang SET lang = %s WHERE id = %s"
        val = (lan, callback.from_user.id)
        ans2 = database.insert(quer, val)
        if ans2 == 0:
            await callback.answer(lang.same_lang)
        else:
            # await callback.message.answer("Database was updated!")
            await bot.send_message(callback.from_user.id, lang.done, reply_markup=admin_kb.kb_maker(lang))
            await callback.answer()

@dp.callback_query_handler(Text(startswith="chl_"))
async def change_lang_user(callback : types.CallbackQuery):
    lan = callback.data.split("_")[1]
    lang = get_lang(callback.from_user.id, lan, True)
    quer = "SELECT * FROM lang WHERE id = %s"
    val = (callback.from_user.id, )
    ans = database.select(quer, val)
    if ans == []:
        quer = "INSERT INTO lang (id, lang) VALUES (%s, %s)"
        val = (callback.from_user.id, lan)
        ans1 = database.insert(quer, val)
        if ans1 == 0:
            await callback.message.answer(lang.error + " #17")
            await callback.answer(lang.error + " #17")
        else:
            await bot.send_message(callback.from_user.id, lang.done, reply_markup=user_kb.kb_maker(lang))
            await callback.answer(lang.done)
    else:
        quer = "UPDATE lang SET lang = %s WHERE id = %s"
        val = (lan, callback.from_user.id)
        ans2 = database.insert(quer, val)
        if ans2 == 0:
            await callback.answer(lang.same_lang)
        else:
            # await callback.message.answer("Database was updated!")
            await bot.send_message(callback.from_user.id, lang.done, reply_markup=user_kb.kb_maker(lang))
            await callback.answer()

@dp.callback_query_handler(Text(startswith="rate_"))
async def rate_user(callback : types.CallbackQuery):
    lang = get_lang(callback.from_user.id, callback.from_user.language_code)
    # print("rate works fine for now!")
    rate, ticket = callback.data.split("_")[1:3]
    rate, ticket = int(rate), int(ticket)
    if rate > 3:
        quer = "Update finished SET rate = %s, message = %s WHERE id = %s"
        val = (rate, "Good rate", ticket)
        ans = database.insert(quer, val)
        if ans == 0:
            await callback.answer(lang.error + " #21")
        else:
            await callback.message.edit_text(lang.feedback)
            await callback.answer(lang.thanks)
            # await callback.message.delete()
    else:
        quer = "UPDATE finished SET rate = %s, writing = %s WHERE id = %s"
        val = (rate, 1, ticket)
        ans = database.insert(quer, val)
        await callback.message.edit_text(lang.feedback)
        await callback.message.answer(lang.tell_report, reply_markup=user_kb.no_kb(lang))
        await callback.answer()

    # FOR RATE CALCULATION 
    quer = "SELECT admin_id FROM finished WHERE id = %s"
    val = (ticket, )
    adq = database.select_one(quer, val)
    if adq == {}:
        await callback.message.answer(lang.error + " #98")
    else:
        quer = "SELECT admin_id, admin_name, con_count, avg_rate FROM admins WHERE admin_id = %s"
        val = (adq["admin_id"], )
        adm = database.select_one(quer, val)
        if adm != {}:
            old_sum = adm["avg_rate"] * adm["con_count"]
            new_count = adm["con_count"] + 1
            new_avg = ( old_sum + rate ) / new_count
            quer = "UPDATE admins SET avg_rate = %s, con_count = %s WHERE admin_id = %s"
            val = (new_avg, new_count, adq["admin_id"])
            last_query = database.insert(quer, val)
            if last_query == 0:
                await callback.message.answer(lang.error + " #97")
        else:
            await callback.message.answer(lang.error + " #96")

        
@dp.callback_query_handler()
async def any_callback_final(callback : types.CallbackQuery):
    await callback.answer("NO!")