from helpers.api_connection import get_lang, register, register_db, get_lang_str, set_lang, make_super, add_message, set_status, close_status, get_status, add_proove_photo, add_proove_description, get_msg_before_closing, set_choosen_status
from helpers.filter import Is_admin, Share_tel, Have_status
from aiogram import types
from keyboards import user_kb
from main import dp
from main import bot
from lang import lang
from aiogram.dispatcher.filters import Text
from helpers.QRreader import read_qr_code
        
class bot_defaults:
    video = "BAACAgIAAxkBAAIU_2OFmQgy1vNZgJi0McS8XPDQJxKeAAJtHwACqjkwSFImk3NqnjRgKwQ"

bot_d = bot_defaults()

# @dp.message_handler( Is_admin(), Text(equals=lang.gal( "chooseUser" )) )
# async def choose_user(message: types.Message):
#     lang = get_lang(message.from_user.id, message.from_user.language_code)

# ___________________________________________________________________Login proccess_____________________________________________________________________

@dp.message_handler( Share_tel(), commands=['start', 'help'] )
async def send_welcome( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.wellcome, reply_markup=user_kb.kb_maker(lan) )


@dp.message_handler( commands=['start', 'help'] )
async def send_welcome_known( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply( lan.wellcome, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Share_tel(), content_types=['contact'] )
async def tel_handler( message: types.Message ):
    lan = get_lang( message.from_id, message.from_user.language_code )
    if ( message.contact.user_id != message.from_user.id ):
        await message.answer( "Это не ваш контакт / Bu sizning kontaktingiz emas", reply_markup=user_kb.kb_maker(lan) )
    else:
        register_db( message.from_user.full_name, message.from_user.id, message.contact.phone_number)
        # Register contact (message.from_user.id, message.from_user.full_name, message.contact.phone_number) 
        await message.answer( "Выберите язык / Tilni tanlang", reply_markup = user_kb.lang_kb() ) 

@dp.message_handler( Share_tel() )
async def must_share( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.please_contact, reply_markup=user_kb.kb_maker(lan) )


# ___________________________________________________________________Main proccess_____________________________________________________________________



@dp.message_handler( Have_status(), Text(equals=lang.gal("close")) )
async def reject_status( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    close_status( message.from_user.id )
    await message.answer( lan.closed, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Have_status(), content_types=['text'] )
async def block_status( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if status == 5:
        await message.answer( lan.upload_photo )
    elif status == 6:
        msg_id, chat_id = get_msg_before_closing( message.from_user.id )
        add_proove_description( message.from_user.id, message.text )
        set_status( message.from_user.id, 0 )
        # to do should get msg_id and chat_id then edit it.
        await bot.edit_message_text( lan.done, chat_id, msg_id, reply_markup=types.InlineKeyboardMarkup() )
        await message.answer( lan.done, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Text(equals=lang.gal("menu")) )
async def send_menu( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Text(equals=lang.gal("lang")) )
async def menu_handler( message: types.Message ):
    lan_str = message.from_user.language_code
    if( message.text == lang.ru.lang ):
        lan_str = "ru"
    elif( message.text == lang.uz.lang ):
        lan_str = "uz"
    lan = set_lang( message.from_user.id, lan_str )
    await message.answer( lan.done, reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Text(equals=lang.gal("check")) )
async def check_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.send_photo )


@dp.message_handler( commands=['superadmin'] )
async def send_welcome( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    make_super( message.from_user.id )
    await message.reply( "You become superadmin", reply_markup=user_kb.menu_kb(lan) )


@dp.message_handler( Is_admin(), content_types=['video'] )
async def video_uploader( message: types.Message ):
    bot_d.video = message.video.file_id
    await message.answer( "Default video was updated!\n" + bot_d.video )


@dp.message_handler( Text(equals=lang.gal("instructions")) )
async def instructions_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.reply_video( bot_d.video )


@dp.message_handler( Text(equals=lang.gal("contact_us")) )
async def contacts_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.contacts )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("settings")) )
async def admin_settings_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.admin_settings_kb(lan) )


@dp.message_handler( Is_admin(), Text(equals=lang.gal("change_video")) )
async def change_video_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.send_video )


@dp.message_handler( Text(equals=lang.gal("settings")) )
async def settings_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    await message.answer( lan.done, reply_markup=user_kb.settings_kb(lan) )


async def proove_file_worker( message: types.Message, file: types.Document, filename:str, lan:lang.ru ):
    await file.download( destination_file="prooves/" + filename )
    add_proove_photo( message.from_user.id, filename )
    set_status( message.from_user.id, 6 )
    await message.answer( lan.photo_desc, reply_markup=user_kb.reject(lan) )


@dp.message_handler( Have_status(), content_types=['document'] )
async def doc_proove_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if ( status == 5 ):
        filename = message.document.file_name
        if( message.document.mime_type in ["image/png", "image/jpeg"] ):
            await proove_file_worker( message, message.document, filename, lan )
    else:
        await message.answer( lan.alrd_uploded )


@dp.message_handler( Have_status(), content_types=['photo'] )
async def proove_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    status = get_status( message.from_user.id )
    if ( status == 5 ):
        filename = message.photo[-1].file_unique_id + ".jpg"
        await proove_file_worker( message, message.photo[-1], filename, lan )
    else:
        await message.answer( lan.alrd_uploded )

async def photo_file_worker(message: types.Message, file: types.Document, filename:str, lan:lang.ru):
    await file.download( destination_file="downloads/" + filename )
    val = str( read_qr_code( filename ) )
    if val == "":
        await message.reply( lan.not_found )
    else:
        msg = await message.reply( val )
        add_message( message.from_user.id, filename, msg.message_id, message.chat.id )
        await bot.edit_message_reply_markup(message.chat.id, msg.message_id, reply_markup = user_kb.qr_kb(lan, msg.message_id, message.chat.id))


@dp.message_handler( content_types=['photo'] )
async def photo_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    filename = message.photo[-1].file_unique_id + ".jpg"
    await photo_file_worker(message, message.photo[-1], filename, lan)

    # print( await message.photo[-1].get_url() )
    # Get photo url

    # print(message.photo)
    # [
    #   <PhotoSize {"file_id": "AgACAgIAAxkBAAIUXGODcRx0FYBqtBovnwABFkfDC4HzuAACPL8xG7ljGUhT8sFhYY4BOQEAAwIAA3MAAysE", "file_unique_id": "AQADPL8xG7ljGUh4", "file_size": 810, "width": 90, "height": 47}>, 
    #   <PhotoSize {"file_id": "AgACAgIAAxkBAAIUXGODcRx0FYBqtBovnwABFkfDC4HzuAACPL8xG7ljGUhT8sFhYY4BOQEAAwIAA20AAysE", "file_unique_id": "AQADPL8xG7ljGUhy", "file_size": 7752, "width": 320, "height": 168}>, 
    #   <PhotoSize {"file_id": "AgACAgIAAxkBAAIUXGODcRx0FYBqtBovnwABFkfDC4HzuAACPL8xG7ljGUhT8sFhYY4BOQEAAwIAA3gAAysE", "file_unique_id": "AQADPL8xG7ljGUh9", "file_size": 39940, "width": 800, "height": 420}>, 
    #   <PhotoSize {"file_id": "AgACAgIAAxkBAAIUXGODcRx0FYBqtBovnwABFkfDC4HzuAACPL8xG7ljGUhT8sFhYY4BOQEAAwIAA3kAAysE", "file_unique_id": "AQADPL8xG7ljGUh-", "file_size": 71464, "width": 1200, "height": 630}>
    # ]


@dp.message_handler( content_types=['document'] )
async def file_handler( message: types.Message ):
    lan = get_lang( message.from_user.id, message.from_user.language_code )
    filename = message.document.file_name
    if( message.document.mime_type in ["image/png", "image/jpeg"] ):
        await photo_file_worker(message, message.document, filename, lan)

    # print( message.document )
    # {
    #     "file_name": "Alisheraka.jpg", 
    #     "mime_type": "image/jpeg", 
    #     "thumb": {
    #         "file_id": "AAMCAgADGQEAAhdSY4cakYd2bhdo87NWI0RNYu808FQAAgIoAAKfazlIQO0AAUJmjpUUAQAHbQADKwQ", 
    #         "file_unique_id": "AQADAigAAp9rOUhy", 
    #         "file_size": 20629, 
    #         "width": 320, 
    #         "height": 179
    #     }, 
    #     "file_id": "BQACAgIAAxkBAAIXUmOHGpGHdm4XaPOzViNETWLvNPBUAAICKAACn2s5SEDtAAFCZo6VFCsE", 
    #     "file_unique_id": "AgADAigAAp9rOUg", 
    #     "file_size": 693685
    # }


@dp.message_handler()
async def last_handler( message: types.Message ):
    await message.answer( "Last handler" )


# _______________________________________________________________ Callback handlers _______________________________________________________________

@dp.callback_query_handler( Have_status() )
async def last_callback_handler( callback : types.CallbackQuery ):
    lan = get_lang( callback.from_user.id, callback.from_user.language_code )
    await callback.answer( lan.not_finished )


# Accept inline keyboard handler
@dp.callback_query_handler( Text(startswith="qr_") )
async def accept( callback : types.CallbackQuery ):
    msg_id, chat_id  = callback.data.split("_")[1:3]
    lan = get_lang( callback.from_user.id, callback.from_user.language_code )
    set_status( callback.from_user.id, 5 )
    set_choosen_status( msg_id, chat_id )
    await callback.message.answer( lan.send_proove, reply_markup=user_kb.reject(lan) )
    await callback.answer( lan.done )
