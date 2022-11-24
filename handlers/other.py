from database.database import calc_admin, database, get_lang
from aiogram import types
from keyboards import user_kb, admin_kb
from main import dp, bot

from helpers.filter import Is_admin

print("Others are connected!")


async def alert_admin():
    quer = "SELECT * FROM admins"
    ans = database.select(quer)
    if ans != []:
        quer = "SELECT COUNT(*) AS users_count FROM user_messages"
        ans2 = database.select_one(quer)
        if ans2 != {}:
            users_count = ans2["users_count"]
            for adm in ans:
                lang = get_lang(adm[0])
                if users_count == 1:
                    await bot.send_message(adm[0], lang.hanging_user)
                else:
                    await bot.send_message(adm[0], lang.hanging_many % str(users_count))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    lan = get_lang(message.from_user.id, message.from_user.language_code)
    await message.reply(lan.wellcome, reply_markup=user_kb.kb_maker(lan))



@dp.message_handler(commands=['superadmin'])
async def super_admin(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    quer1 = "DELETE FROM user_messages WHERE user_id = %s"
    quer2 = "DELETE FROM conversation WHERE user_id = %s"
    adm = "SELECT admin_id, super FROM admins WHERE admin_id = %s"
    val = (message.from_user.id, )
    database.insert(quer1, val)
    database.insert(quer2, val)
    ans = database.select_one(adm, val)
    if ans == {}:
        adm2 = "INSERT INTO admins (admin_id, admin_name, con_count, avg_rate, super) VALUES (%s, %s, %s, %s, %s)"
        val2 = (message.from_user.id, message.from_user.first_name, 0, 0.0, 1)
        ans2 = database.insert(adm2, val2)
        if ans2 == 0:
            await message.answer(lang.error + "#71")
        else:
            await message.reply(lang.super_admin, reply_markup=admin_kb.super_kb(lang))
    elif ans["super"] == 1:
        await message.reply(lang.was_admin, reply_markup=admin_kb.super_kb(lang))
    else:
        quer3 = "UPDATE admins SET super = %s WHERE admin_id = %s"
        val3 = (1, message.from_user.id)
        ans3 = database.insert(quer3, val3)
        if ans3 == 0:
            await message.answer(lang.error + "#72")
        else:
            await message.reply(lang.super_admin, reply_markup=admin_kb.super_kb(lang))
    
    if calc_admin(message.from_user.id) != 0:
        await message.answer(lang.error + " 73")



@dp.message_handler(commands=['admin'])
async def become_admin(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    quer1 = "DELETE FROM user_messages WHERE user_id = %s"
    quer2 = "DELETE FROM conversation WHERE user_id = %s"
    adm = "SELECT admin_id FROM admins WHERE admin_id = %s"
    val = (message.from_user.id, )
    database.insert(quer1, val)
    database.insert(quer2, val)
    ans = database.select(adm, val)
    if ans == []:
        adm2 = "INSERT INTO admins (admin_id, admin_name, con_count, avg_rate) VALUES (%s, %s, %s, %s)"
        val2 = (message.from_user.id, message.from_user.first_name, 0, 0.0)
        database.insert(adm2, val2)
        await message.reply(lang.be_admin, reply_markup=admin_kb.kb_maker(lang))
    else:
        await message.reply(lang.was_admin, reply_markup=admin_kb.kb_maker(lang))
        
    if calc_admin(message.from_user.id) != 0:
        await message.answer(lang.error + " 73")

@dp.message_handler( Is_admin(), content_types = [types.ContentType.TEXT] )
async def text_handler(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    adm = "SELECT admin_id FROM admins WHERE admin_id = %s"
    val = (message.from_user.id, )
    ans = database.select(adm, val)
    admin_id = ans[0][0]
    query = "SELECT * FROM conversation WHERE admin_id = %s"
    v = (admin_id, )
    ans2 = database.select(query, v)
    if ans2 == []:
        await message.answer(lang.should_choose)
    else: 
        user_id = ans2[0][1]
        await bot.send_message(user_id, message.text)
        # await bot.delete_message()



@dp.message_handler( content_types = [types.ContentType.TEXT] )
async def text_handler(message: types.Message):
    lang = get_lang(message.from_user.id, message.from_user.language_code)
    query = "SELECT * FROM user_messages WHERE user_id = %s"
    v = (message.from_user.id, )
    ans2 = database.select(query, v)
    if ans2 == []:
        query = "SELECT * FROM conversation WHERE user_id = %s"
        v = (message.from_user.id, )
        ans2_a = database.select(query, v)
        if ans2_a == []:
            qu = "INSERT INTO user_messages (user_id, chat_id, message, user_name) VALUES (%s, %s, %s, %s)"
            va = (message.from_user.id, message.chat.id, message.text, message.from_user.full_name)
            ans3 = database.insert(qu, va)
            if ans3 != 0:
                await message.answer(lang.waiting, reply_markup=user_kb.kb_maker(lang))
                await alert_admin()
            else:
                await message.answer(lang.fix_that + " #1", reply_markup=user_kb.kb_maker(lang))
            
        else:
            await bot.send_message(ans2_a[0][0], text=message.text)
    else:
        qu = "UPDATE user_messages SET message = %s WHERE user_id = %s"
        va = (str(ans2[0][2]) + "\n" + message.text,  message.from_user.id)
        an = database.insert(qu, va)
        if an != 0:
            await message.answer(lang.mes_update, reply_markup=user_kb.kb_maker(lang))
        else:
            await message.answer(lang.fix_that + " #2", reply_markup=user_kb.kb_maker(lang))