import database.selfbase as sb
from lang import lang
from datetime import datetime

def get_user_phone( user_id ):
    user = sb.get_user(user_id)
    return user.tel

def register_db(user_id, full_name, phone, reg_res):
    user = sb.get_user(user_id)
    role = reg_res["role"]
    if user:
        if user.role == "Seller" and role == "Store Owner":
            user.updated = datetime.now()
            user.seller_id = 0
            user.hrid = reg_res["user"]["hrid"]
            user.role = role
            user.is_admin = 1
        elif user.role == "Store Owner" and role == "Seller":
            user.updated = datetime.now()
            user.seller_id = reg_res["user"]["id"]
            user.role = role
            user.hrid = 0
            user.is_admin = 0
    else:
        if role == "Store Owner":
            user = sb.insert_user( full_name, user_id, phone, 0, 1 )
            user.role = role
            user.hrid = reg_res["user"]["hrid"]
        elif role == "Seller":
            user = sb.insert_user( full_name, user_id, phone, reg_res["user"]["id"], 0 )
            user.role = role
            user.hrid = 0

    

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
    user.role = "Store Owner"
    user.hrid = 1034418716553026

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
    msg.proove_file, msg.proved, msg.file_type = filename, 1, file_type

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
    return msg.prod_id, msg.proove_file, msg.rejected, msg.file_type # prod_id, filename, rejected, file_type

def get_seller_id(user_id):
    user = sb.get_user(user_id)
    return user.seller_id

def check_admin(user_id):
    user = sb.get_user(user_id)
    if user:
        return user.role == "Store Owner"
    return False

def check_user(user_id):
    user = sb.get_user(user_id)
    if user:
        return user.role == "Seller"
    return False

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

def del_msg(msg_id, chat_id):
    sb.del_msg(msg_id, chat_id)

def calc_update(user_id):
    user = sb.get_user(user_id)
    diff = datetime.now() - user.updated
    return diff.total_seconds() > 300 #5 minutes

def set_user_choosen( owner_id, del_id, del_seller_id, del_phone):
    user = sb.get_user( owner_id )
    user.choosen_id = del_id
    user.choosen_seller_id = del_seller_id
    user.choosen_phone = del_phone
    user.status = 1

def dont_del_user( owner_id ):
    user = sb.get_user( owner_id )
    user.choosen_id = 0
    user.choosen_seller_id = 0
    user.choosen_phone = 0
    user.status = 0

def get_del_user( owner_id ):
    user = sb.get_user( owner_id )
    sb.del_user( user.choosen_phone )
    return user.hrid, user.choosen_id

def set_status_zero( user_id ):
    user = sb.get_user(user_id)
    user.status = 0

def set_choosen_user_name( owner_id, user_name ):
    owner = sb.get_user( owner_id )
    owner.choosen_user_name = user_name

def get_choosen_user_name( owner_id ):
    owner = sb.get_user( owner_id )
    return owner.choosen_user_name

def get_hrid( owner_id ):
    owner = sb.get_user( owner_id )
    return owner.hrid
