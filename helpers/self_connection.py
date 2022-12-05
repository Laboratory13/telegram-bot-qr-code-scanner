import database.selfbase as sb
from lang import lang

def check_phone(phone):
    return sb.check_phone(phone)

def connect_base(team):
    sb.connect(team)

def register_db(full_name, tg_id, phone, seller_id, is_admin=0, lang="ru"):
    sb.insert_user( full_name, tg_id, phone, seller_id, is_admin, lang )

def set_lang(user_id, lan):
    user = sb.get_user(user_id)
    user.lang = lan
    return lang.gl(lan)

def get_lang(user_id, def_lan:str = "ru", get_defaul:bool = False) -> lang.ru:
    user = sb.get_user( user_id )
    if get_defaul:
        return lang.gl( def_lan )
    if user:
        return lang.gl( user.lang )
    return lang.gl(def_lan)

def get_lang_str(user_id):
    user = sb.get_user(user_id)
    return user.lang

def make_super(user_id):
    user = sb.get_user(user_id)
    user.is_admin = 1

def set_status( id, status, msg_id, chat_id ):
    user = sb.get_user( id )
    user.status, user.msg_id, user.chat_id = status, msg_id, chat_id

def get_status(id):
    user = sb.get_user( id )
    return user.status

def close_status(id, msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proved = 0
    set_status(id, 0, 0, 0)

def add_message(id, file_id, msg_id, chat_id, prod_id):
    sb.insert_msg(id, file_id, msg_id, chat_id, prod_id)

def add_proove_photo(user_id, filename, msg_id, chat_id, file_type):
    msg = sb.get_msg(msg_id, chat_id)
    msg.file_name, msg.proved, msg.file_type = filename, 1, file_type

def add_proove_description(user_id, text, msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proove_desc, msg.proved = text, 2

def set_choosen_status(msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proved = 3

def get_msg_id(user_id):
    user = sb.get_user(user_id)
    return user.msg_id, user.chat_id

def set_rejected_status(msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    msg.proved, msg.rejected = 1, 1

def get_prod_id(msg_id, chat_id):
    msg = sb.get_msg(msg_id, chat_id)
    return msg.prod_id, msg.proove_file, msg.rejected, msg.file_type

def get_seller_id(user_id):
    user = sb.get_user(user_id)
    return user.seller_id

def check_admin(user_id):
    user = sb.get_user(user_id)
    if user:
        return user.is_admin
    return 0

def check_has_tel(user_id):
    user = sb.get_user(user_id)
    if user == None:
        return False
    return user.tel != "0"

def check_has_status(user_id):
    user = sb.get_user(user_id)
    if user == None:
        return False
    else:
        return user.status != 0
