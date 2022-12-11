from helpers.self_connection import *
from helpers.filter import *
import helpers.joha_api as japi
from aiogram import types
from keyboards import user_kb
from main import dp
from main import bot
from lang import lang
from aiogram.dispatcher.filters import Text
from helpers.QRreader import read_qr_code
        
class bot_defaults:
    video = ""
    file = types.input_file.InputFile("default.mp4")
    print(file.filename)

bot_d = bot_defaults()

async def startup(e):
    print( "Bot is running..." )

# ___________________________________________________________________General functions_____________________________________________________________________

def check_number(text):
    t = str(text)
    number = str( int(''.join(filter(str.isdigit, t))) )
                
    if len(number) == 12:
        return number
    return False


async def proove_file_worker( message: types.Message, file: types.Document, filename:str, lan:lang.ru, file_type ):
    await file.download( destination_file="prooved/" + filename )
    msg_id, chat_id = get_msg_id( message.from_user.id )
    add_proove_photo( message.from_user.id, filename, msg_id, chat_id, file_type )
    set_status( message.from_user.id, 6, msg_id, chat_id )
    await message.answer( lan.photo_desc, reply_markup=user_kb.reject(lan) )


async def finish_selling( message:types.Message, msg_id, chat_id, lan:lang.ru ):
    add_proove_description( message.from_user.id, message.text, msg_id, chat_id )
    set_status( message.from_user.id, 0, msg_id, chat_id )
    prod_id, filename, rejected, file_type = get_prod_id( msg_id, chat_id )
    seller_id = get_seller_id( message.from_user.id )
    # print("sending to joha: ", prod_id, seller_id, message.text, "x.png" if rejected else filename, file_type, 0 if rejected else 1)
    ans = japi.sell_reports( prod_id, seller_id, message.text, "x.png" if rejected == 1 else filename, file_type, 0 if rejected else 1 )
    # send_report( prod_id, seller_id, message.text, filename, file_type, 0 if rejected else 1 )
    await bot.edit_message_text( lan.done, chat_id, msg_id, reply_markup=types.InlineKeyboardMarkup() )
    if( "error" in ans ):
        await message.answer( lan.prod_sold, reply_markup=user_kb.menu_kb(lan) )
    else:
        await message.answer( lan.done, reply_markup=user_kb.menu_kb(lan) )
    # {'error': True, 'message': {'product_code_id': ['validation.required'], 'seller_id': ['validation.required'], 'action': ['validation.required']}}


async def photo_file_worker(message: types.Message, file: types.Document, filename:str, lan:lang.ru):
    await file.download( destination_file="downloads/" + filename )
    hash = str( read_qr_code( filename ) )
    if hash == "":
        await message.reply( lan.not_found )
        # to do: delete photo from disk to free space in disk
    else:
        res = japi.hash_check(hash)
        val, text = japi.get_print_values(res, lan)
        if val == 1:
            await message.reply( lan.prod_not_found )
            # to do: delete photo from disk to free space in disk
        elif val == 2:
            await message.reply( lan.prod_sold + "\n" + text )
            # to do: delete photo from disk to free space in disk
        else:
            prod_id = res["order"]["id"]
            msg = await message.reply( text )
            add_message( message.from_user.id, filename, msg.message_id, message.chat.id, prod_id )
            await bot.edit_message_reply_markup( message.chat.id, msg.message_id, reply_markup = user_kb.qr_kb(lan, msg.message_id, message.chat.id) )


# ___________________________________________________________________Login proccess_____________________________________________________________________


@dp.message_handler( Share_tel(), commands=['start', 'help'] )
async def send_welcome( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.wellcome, reply_markup=user_kb.kb_maker(lan) )


@dp.message_handler( Share_tel(), content_types=['contact'] )
async def tel_handler( message: types.Message ):
    lan = get_lang( message.from_id, message.from_user.language_code )
    if ( message.contact.user_id != message.from_user.id ):
        await message.answer( "Это не ваш контакт / Bu sizning kontaktingiz emas", reply_markup=user_kb.kb_maker(lan) )
    else:
        # Register contact (message.from_user.id, message.from_user.full_name, message.contact.phone_number)
        phone = str(int(message.contact.phone_number))
        reg_res = japi.register( phone, message.from_user.id )
        if "user" in reg_res:
            register_db( message.from_user.id, message.from_user.full_name, phone, reg_res )
            await message.answer( "Выберите язык / Tilni tanlang", reply_markup = user_kb.lang_kb() ) 
        else:
            await message.answer( "Вы не сможете пользоватся с этим ботом!\nSiz ushbu bottan foydalana olmaysiz!" )


@dp.message_handler( Share_tel() )
async def must_share( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.please_contact, reply_markup=user_kb.kb_maker(lan) )


# _______________________________________________________________Register each 5 minutes______________________________________________________________


@dp.message_handler( Not_allowed() )
async def check_allowed( message:types.Message ):
    await message.answer( "Вы не сможете пользоватся с этим ботом!\nSiz ushbu bottan foydalana olmaysiz!" )


# ___________________________________________________________________Have Status_____________________________________________________________________


@dp.message_handler( Have_status(), Text(equals=lang.gal("yes")) )
async def accept_status( message: types.Message ):
    status = get_status( message.from_user.id )
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    if status == 1:
        hrid, del_id = get_del_user( message.from_user.id )
        ans = japi.del_team_member( hrid, del_id )
        set_status_zero( message.from_user.id )
        if "error" in ans:
            await message.answer(ans["message"])
        else:
            await message.answer( lan.done, reply_markup=user_kb.admin_menu_kb(lan) )
    else:
        await message.reply( lan.last )


@dp.message_handler( Have_status(), Text(equals=lang.gal("close")) )
async def reject_status( message: types.Message ):
    status = get_status( message.from_user.id )
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    if status in [5, 6]: # user is registering qr-code 
        msg_id, chat_id = get_msg_id( message.from_user.id )
        close_status( message.from_user.id, msg_id, chat_id )
        await message.answer( lan.closed, reply_markup=user_kb.menu_kb(lan) )
    elif status == 1: # status 1: user choosen to delete
        dont_del_user( message.from_user.id )
        await message.answer( lan.closed, reply_markup=user_kb.admin_menu_kb(lan) )
    elif status == 2: # status 2: owner adding new user typing name
        set_status_zero( message.from_user.id )
        await message.answer( lan.closed, reply_markup=user_kb.admin_menu_kb(lan) )
    elif status == 3: # status 3: owner adding new user typing phone
        set_status_zero( message.from_user.id )
        set_choosen_user_name( message.from_user.id, "")
        await message.answer( lan.closed, reply_markup=user_kb.admin_menu_kb(lan) )
    else:
        await message.reply( lan.last )


@dp.message_handler( Have_status(), Text(equals=lang.gal("skip")) )
async def skip_status( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if status == 5:
        msg_id, chat_id = get_msg_id( message.from_user.id )
        filename = "x.png"
        add_proove_photo( message.from_user.id, filename, msg_id, chat_id, "image/png" )
        set_status( message.from_user.id, 6, msg_id, chat_id )
        await message.answer( lan.photo_desc, reply_markup=user_kb.reject(lan) )
    elif status == 6:
        msg_id, chat_id = get_msg_id( message.from_user.id )
        filename = "x.png"
        await finish_selling(message, msg_id, chat_id, lan)
    else:
        await message.reply( lan.last )


@dp.message_handler( Have_status(), content_types=['text'] )
async def block_status( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if status == 5:
        msg_id, chat_id = get_msg_id( message.from_user.id )
        await message.answer( lan.upload_photo )
    elif status == 6:
        msg_id, chat_id = get_msg_id( message.from_user.id )
        await finish_selling(message, msg_id, chat_id, lan)
    elif status == 2:
        set_status(message.from_user.id, 3, 0, 0)
        set_choosen_user_name( message.from_user.id, message.text )
        await message.answer( lan.type_phone, reply_markup=user_kb.admin_close(lan) )
    elif status == 3:
        number = check_number(message.text)
        if number:
            user_name = get_choosen_user_name( message.from_user.id )
            hrid = get_hrid( message.from_user.id )
            ans = japi.add_team_member(hrid, user_name, number)
            if "error" in ans:
                await message.answer(ans["message"])
            else:
                set_status_zero( message.from_user.id )
                await message.answer( lan.done, reply_markup=user_kb.admin_menu_kb(lan) )
        else:
            await message.answer( lan.type_phone, reply_markup=user_kb.admin_close(lan) )
    else:
        await message.reply( lan.last )


@dp.message_handler( Have_status(), content_types=['photo'] )
async def proove_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if status == 5:
        filename = message.photo[-1].file_unique_id + ".jpg"
        await proove_file_worker( message, message.photo[-1], filename, lan, "image/jpeg" )
    else:
        await message.reply( lan.last )


@dp.message_handler( Have_status(), content_types=['document'] )
async def doc_proove_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if ( status == 5 ):
        filename = message.document.file_unique_id + "_" + message.document.file_name
        if( message.document.mime_type in ["image/png", "image/jpeg"] ):
            await proove_file_worker( message, message.document, filename, lan, message.document.mime_type )
    else:
        await message.reply( lan.last )


# ___________________________________________________________________Admin functions_____________________________________________________________________


@dp.message_handler( Is_admin(), commands=['start', 'help'] )
async def send_welcome_known( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.wellcome, reply_markup=user_kb.admin_menu_kb(lan) )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("lang")) )
async def menu_handler( message: types.Message ):
    lan_str = message.from_user.language_code
    if( message.text == lang.ru.lang ):
        lan_str = "ru"
    elif( message.text == lang.uz.lang ):
        lan_str = "uz"
    lan = set_lang( message.from_user.id, lan_str )
    await message.answer( lan.done, reply_markup=user_kb.admin_menu_kb(lan) )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("menu")) )
async def send_menu( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.admin_menu_kb(lan) )


@dp.message_handler( Is_admin(), content_types=['video'] )
async def video_uploader( message: types.Message ):
    bot_d.video = message.video.file_id
    await message.answer( "Default video was updated!\n" + bot_d.video )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("settings")) )
async def admin_settings_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.admin_settings_kb(lan) )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("change_video")) )
async def change_video_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.send_video )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("get_team")) )
async def get_team_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    hrid = get_hrid( message.from_user.id )
    users = japi.get_team( hrid )
    if "error" in users:
        await message.answer( users["message"], reply_markup=user_kb.admin_menu_kb(lan) )
    else:
        await message.answer( lan.choose_one, reply_markup=user_kb.to_list(users) )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("add_user")) )
async def add_user_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    set_status( message.from_user.id, 2, 0, 0)
    await message.answer( lan.type_name, reply_markup=user_kb.admin_close(lan) )


# ___________________________________________________________________Main process_____________________________________________________________________


@dp.message_handler( Is_user(), commands=['start', 'help'] )
async def send_welcome_known( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.wellcome, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Is_user(), Text(equals=lang.gal("lang")) )
async def menu_handler( message: types.Message ):
    lan_str = message.from_user.language_code
    if( message.text == lang.ru.lang ):
        lan_str = "ru"
    elif( message.text == lang.uz.lang ):
        lan_str = "uz"
    lan = set_lang( message.from_user.id, lan_str )
    await message.answer( lan.done, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Is_user(), Text(equals=lang.gal("menu")) )
async def send_menu( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Is_user(), Text(equals=lang.gal("check")) )
async def check_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.send_photo )


@dp.message_handler( Text(equals=lang.gal("instructions")) )
async def instructions_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    if bot_d.video:
        await message.reply_video( bot_d.video )
    else:
        vid = await message.reply_video( bot_d.file )
        bot_d.video = vid.video.file_id
    


@dp.message_handler( Text(equals=lang.gal("contact_us")) )
async def contacts_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.contacts )


@dp.message_handler( Is_user(), Text(equals=lang.gal("settings")) )
async def settings_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.settings_kb(lan) )


@dp.message_handler( Is_user(), content_types=['photo'] )
async def photo_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    filename = message.photo[-1].file_unique_id + ".jpg"
    await photo_file_worker(message, message.photo[-1], filename, lan)


@dp.message_handler( Is_user(), content_types=['document'] )
async def file_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    filename = message.document.file_unique_id + "_" + message.document.file_name
    if( message.document.mime_type in ["image/png", "image/jpeg"] ):
        await photo_file_worker(message, message.document, filename, lan)


@dp.message_handler( Is_user(), commands=['superadmin'] )
async def send_welcome( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    make_super( message.from_user.id )
    await message.reply( "You become superadmin", reply_markup=user_kb.admin_menu_kb(lan) )


# _______________________________________________________________ Last handlers _______________________________________________________________


@dp.message_handler()
async def last_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.last )


@dp.message_handler( content_types=['photo'] )
async def last_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.last )


# _______________________________________________________________ Callback handlers _______________________________________________________________


@dp.callback_query_handler( Have_status() )
async def last_callback_handler( callback : types.CallbackQuery ):
    lan = get_lang( callback.from_user.id, callback.from_user.language_code )
    await callback.answer( lan.last )


# Accept inline keyboard handler
@dp.callback_query_handler( Text(startswith="qr_") )
async def accept( callback : types.CallbackQuery ):
    msg_id, chat_id = callback.data.split("_")[1:3]
    lan = get_lang( callback.from_user.id, callback.from_user.language_code )
    set_status( callback.from_user.id, 5, msg_id, chat_id )
    set_choosen_status( msg_id, chat_id )
    await callback.message.answer( lan.send_proove, reply_markup=user_kb.reject(lan) )
    await callback.answer( lan.done )


# Reject inline keyboard handler
@dp.callback_query_handler( Text(startswith="ro_") )
async def reject( callback : types.CallbackQuery ):
    msg_id, chat_id = callback.data.split("_")[1:3]
    lan = get_lang( callback.from_user.id, callback.from_user.language_code )
    set_status( callback.from_user.id, 6, msg_id, chat_id )
    set_rejected_status( msg_id, chat_id )
    await callback.message.answer( lan.reason, reply_markup=user_kb.reject(lan) )
    await callback.answer( lan.done )


# Choose user only for admin 
@dp.callback_query_handler( Text(startswith="us_") )
async def reject( callback : types.CallbackQuery ):
    phone, seller_id, id = callback.data.split("_")[1:4]
    lan = get_lang( callback.from_user.id, callback.from_user.language_code )
    set_user_choosen( callback.from_user.id, id, seller_id, phone )
    await callback.message.answer( lan.sure + "\n" + phone, reply_markup=user_kb.choice(lan) )
    await callback.answer()