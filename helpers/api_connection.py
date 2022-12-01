from database.database import database
from lang import lang


import requests
import json


url = "https://api.pharmiq.uz/api/v1/bot/register?token=dG9rZW5sa2Rqc2FsMTIza2xhamFzbGtkamFsa2QyMSFBc0Bhc2Q="


def register(full_name, tg_id, phone, is_admin=False, lang="ru"):
    payload={
        'sellerPhone': '998946667788',
        'telegram_id': '22323232',
        'platform': 'website',
        'device': 'desktop',
        'timeZone': '500',
        'browser': 'chrome'
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload,)

    print(response.text)

# register("Jas", "123123213", "9349293492")


def register_db(full_name, tg_id, phone, is_admin=False, lang="ru"):
    quer = "INSERT INTO users (id, full_name, lang, is_admin, tel, status) VALUES (%s, %s, %s, %s, %s, %s)"
    v = ( tg_id, full_name, lang, 1 if is_admin else 0, phone, 0 )
    database.insert(quer, v)


def set_lang(user_id, def_lan:str = "ru"):
    quer = "UPDATE users SET lang = %s WHERE id = %s"
    v = (def_lan, user_id)
    database.insert(quer, v)
    return lang.gl(def_lan)


def get_lang(user_id, def_lan:str = "ru", get_defaul:bool = False) -> lang.ru:
    quer = "SELECT * FROM users WHERE id = %s"
    val = (user_id, )
    ans = database.select_one(quer, val)
    if get_defaul:
        return lang.gl(def_lan)
    if ans == {}:
        return lang.gl(def_lan)
    else:
        return lang.gl( str(ans["lang"]) )

def get_lang_str(user_id:int, def_lang:str = "ru"):
    quer = "SELECT * FROM users WHERE id = %s"
    val = (user_id, )
    ans = database.select_one(quer, val)
    if ans == {}:
        return def_lang
    return str(ans['lang'])


def make_super(user_id:int):
    quer = "UPDATE users SET is_admin = %s WHERE id = %s"
    val = ( 1, user_id )
    database.insert(quer, val)


def set_status(id, status:int):
    quer = "UPDATE users SET status = %s WHERE id = %s"
    val = (status, id)
    database.insert(quer, val)


def get_status(id):
    quer = "SELECT * FROM users WHERE id = %s"
    val = ( id, )
    ans = database.select_one( quer, val )
    return ans["status"]

def close_status(id):
    quer = "UPDATE messages SET proved = %s WHERE user_id = %s AND (proved = %s OR proved = %s)"
    val = ( 0, id, 1, 3 )
    database.insert(quer, val)
    set_status(id, 0)


def add_message(id, file_id, msg_id, chat_id):
    quer = "INSERT INTO messages (msg_id, file_id, user_id, chat_id) VALUES (%s, %s, %s, %s)"
    val = (msg_id, file_id, id, chat_id) 
    database.insert(quer, val)


def add_proove_photo(user_id, filename):
    quer = "UPDATE messages SET proove_file = %s, proved = %s WHERE user_id = %s AND proved = %s"
    val = ( filename, 1, user_id, 3 )
    database.insert(quer, val)


def get_msg_before_closing(user_id):
    quer = "SELECT * FROM messages WHERE user_id = %s AND proved = %s"
    val = ( user_id, 1 )
    ans = database.select_one( quer, val )
    return ans["msg_id"], ans["chat_id"]


def add_proove_description(user_id, text):
    quer = "UPDATE messages SET proove_desc = %s, proved = %s WHERE user_id = %s AND proved = %s"
    val = ( text, 2, user_id, 1 )
    database.insert( quer, val )


def set_choosen_status(msg_id, chat_id):
    quer = "UPDATE messages SET proved = %s WHERE msg_id = %s AND chat_id = %s"
    val = ( 3, msg_id, chat_id )
    database.insert( quer, val )