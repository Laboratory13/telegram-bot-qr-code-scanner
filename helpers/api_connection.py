from database.database import database
import database.selfbase as sb
from lang import lang



def s_register_db(full_name, tg_id, phone, seller_id, is_admin=0, lang="ru"):
    sb.insert_user( tg_id, full_name, lang, is_admin, phone, 0, seller_id )

def register_db(full_name, tg_id, phone, seller_id, is_admin=0, lang="ru"):
    quer = "INSERT INTO users (id, full_name, lang, is_admin, tel, status, seller_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    v = ( tg_id, full_name, lang, is_admin, phone, 0, seller_id )
    database.insert(quer, v)



def s_set_lang(user_id, lan):
    user = sb.get_user(user_id)
    user.lang = lan
    return lang.gl(lan)

def set_lang(user_id, def_lan:str = "ru"):
    quer = "UPDATE users SET lang = %s WHERE id = %s"
    v = (def_lan, user_id)
    database.insert(quer, v)
    return lang.gl(def_lan)



def s_get_lang(user_id, def_lan:str = "ru", get_defaul:bool = False) -> lang.ru:
    user = sb.get_user( user_id )
    if get_defaul:
        return lang.gl( def_lan )
    return lang.gl( user.lang )

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



def s_get_lang_str(user_id):
    user = sb.get_user(user_id)
    return user.lang

def get_lang_str(user_id, def_lang:str = "ru"):
    quer = "SELECT * FROM users WHERE id = %s"
    val = (user_id, )
    ans = database.select_one(quer, val)
    if ans == {}:
        return def_lang
    return str(ans['lang'])



def s_make_super(user_id):
    user = sb.get_user(user_id)
    user.is_admin = 1

def make_super(user_id):
    quer = "UPDATE users SET is_admin = %s WHERE id = %s"
    val = ( 1, user_id )
    database.insert(quer, val)



def s_set_status( id, status, msg_id, chat_id ):
    user = sb.get_user( id )
    user.status, user.msg_id, user.chat_id = status, msg_id, chat_id

def set_status( id, status, msg_id, chat_id ):
    quer = "UPDATE users SET status = %s, msg_id = %s, chat_id = %s WHERE id = %s"
    val = ( status, msg_id, chat_id, id )
    database.insert( quer, val )



def s_get_status(id):
    user = sb.get_user( id )
    return user.status

def get_status(id):
    quer = "SELECT * FROM users WHERE id = %s"
    val = ( id, )
    ans = database.select_one( quer, val )
    return ans["status"]



def s_close_status(id, msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proved = 0
    s_set_status(id, 0, 0, 0)

def close_status(id, msg_id, chat_id):
    quer = "UPDATE messages SET proved = %s WHERE user_id = %s AND msg_id = %s AND chat_id = %s"
    val = ( 0, id, msg_id, chat_id )
    database.insert(quer, val)
    set_status(id, 0, 0, 0)



def s_add_message(id, file_id, msg_id, chat_id, prod_id):
    sb.insert_msg(id, file_id, msg_id, chat_id, prod_id)

def add_message(id, file_id, msg_id, chat_id, prod_id):
    quer = "INSERT INTO messages (msg_id, file_id, user_id, chat_id, prod_id) VALUES (%s, %s, %s, %s, %s)"
    val = (msg_id, file_id, id, chat_id, prod_id) 
    database.insert(quer, val)



def s_add_proove_photo(user_id, filename, msg_id, chat_id, file_type):
    msg = sb.get_msg(msg_id, chat_id)
    msg.file_name, msg.proved, msg.file_type = filename, 1, file_type
    
def add_proove_photo(user_id, filename, msg_id, chat_id, file_type):
    quer = "UPDATE messages SET proove_file = %s, proved = %s, file_type = %s WHERE user_id = %s AND proved = %s AND msg_id = %s AND chat_id = %s"
    val = ( filename, 1, file_type, user_id, 3, msg_id, chat_id )
    database.insert( quer, val )



def s_add_proove_description(user_id, text, msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proove_desc, msg.proved = text, 2

def add_proove_description(user_id, text, msg_id, chat_id):
    quer = "UPDATE messages SET proove_desc = %s, proved = %s WHERE user_id = %s AND msg_id = %s AND chat_id = %s"
    val = ( text, 2, user_id, msg_id, chat_id )
    database.insert( quer, val )



def s_set_choosen_status(msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proved = 3

def set_choosen_status(msg_id, chat_id):
    quer = "UPDATE messages SET proved = %s WHERE msg_id = %s AND chat_id = %s"
    val = ( 3, msg_id, chat_id )
    database.insert( quer, val )



def s_get_msg_id(user_id):
    user = sb.get_user(user_id)
    return user.msg_id, user.chat_id

def get_msg_id(user_id):
    quer = "SELECT * FROM users WHERE id = %s"
    val = ( user_id, )
    ans = database.select_one( quer, val )
    return ans["msg_id"], ans["chat_id"]



def s_set_rejected_status(msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proved, msg.rejected = 1, 1

def set_rejected_status(msg_id, chat_id):
    quer = "UPDATE messages SET proved = %s, rejected = %s WHERE msg_id = %s AND chat_id = %s"
    val = ( 1, 1, msg_id, chat_id )
    database.insert( quer, val )



def s_get_prod_id(msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    return msg.prod_id, msg.proove_file, msg.rejected, msg.file_type

def get_prod_id(msg_id, chat_id):
    quer = "SELECT * FROM messages WHERE msg_id = %s and chat_id = %s"
    val = ( msg_id, chat_id )
    ans = database.select_one( quer, val )
    return ans["prod_id"], ans["proove_file"],  ans["rejected"], ans["file_type"]



def s_get_seller_id(user_id):
    user = sb.get_user(user_id)
    return user.seller_id

def get_seller_id(user_id):
    quer = "SELECT * FROM users WHERE id = %s"
    val = ( user_id, )
    ans = database.select_one( quer, val )
    return ans["seller_id"]



def s_check_admin(user_id):
    user = sb.get_user(user_id)
    if user:
        return user.is_admin
    return 0

def check_admin(user_id):
    adm = "SELECT id FROM users WHERE id = %s AND is_admin = %s"
    val = (user_id, 1)
    ans = database.select_one(adm, val)      
    return ans != {}



def s_check_has_tel(user_id):
    user = sb.get_user(user_id)
    if user == None:
        return False
    return user.tel != "0"

def check_has_tel(user_id):
    quer = "SELECT * FROM users WHERE id = %s"
    val = (user_id, )
    ans = database.select_one(quer, val)
    if ans == {}:
        return False # Has not phone
    return ans["tel"] != ""



def s_check_has_status(user_id):
    user = sb.get_user(user_id)
    if user == None:
        return False
    else:
        return user.status != 0

def check_has_status(user_id):
    quer = "SELECT * FROM users WHERE id = %s"
    val = ( user_id, )
    ans = database.select_one(quer, val)
    if ans == {}:
        return False
    else:
        return ans["status"] != 0