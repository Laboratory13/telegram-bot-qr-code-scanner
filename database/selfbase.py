from datetime import datetime

class User:
    def __init__(self, id, full_name, lang, is_admin, tel = "0", status = 0, msg_id = 0, chat_id = 0, seller_id = 0, role = ""):
        self.id = id
        self.full_name = full_name
        self.lang = lang
        self.is_admin = is_admin
        self.tel = tel
        self.status = status
        self.msg_id = msg_id
        self.chat_id = chat_id
        self.seller_id = seller_id
        self.role = role # "Store Owner" || "Seller"
        self.updated = datetime.now()
        self.hrid = 0
        self.choosen_id = 0
        self.choosen_seller_id = 0
        self.choosen_phone = 0
        self.choosen_user_name = ""
    

class Msg:
    def __init__(self, msg_id, file_name, user_id, chat_id, prod_id, proove_file="", proove_desc="", proved=0, time = datetime.now(), rejected=0, file_type=""):
        self.msg_id = msg_id
        self.file_name = file_name
        self.user_id = user_id
        self.chat_id = chat_id
        self.prod_id = prod_id
        self.proove_file = proove_file
        self.proove_desc = proove_desc
        self.proved = proved
        self.time = time
        self.rejected = rejected
        self.file_type = file_type


users = {}
msgs = {}

def get_user(user_id) -> User:
    if user_id in users:
        return users[user_id]
    return None

def get_msg(msg_id, chat_id) -> Msg:
    key = str(msg_id) + str(chat_id)
    if key in msgs:
        return msgs[key]
    return None

def insert_user(full_name, tg_id, phone, seller_id, is_admin=0, lang="ru") -> User:
    users[tg_id] = User(tg_id, full_name, lang, is_admin, phone, seller_id=seller_id)
    return users[tg_id]
    
def insert_msg(id, file_id, msg_id, chat_id, prod_id):
    key = str(msg_id) + str(chat_id)
    msgs[key] = Msg(msg_id, file_id, id, chat_id, prod_id)
    
def del_msg(msg_id, chat_id):
    key = str( msg_id ) + str( chat_id )
    msgs.pop( key, None )
    
def del_user( phone ):
    key = "0"
    for user in users.keys():
        if users[user].tel == phone:
            key = user
    
    users.pop( key, None )