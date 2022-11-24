from aiogram.dispatcher.filters import Filter
from aiogram import types
from database.database import database

class Is_admin(Filter):
    key = "is_admin"
    async def check(self, message: types.Message):
        adm = "SELECT admin_id FROM admins WHERE admin_id = %s"
        val = (message.from_user.id, )
        ans = database.select(adm, val)        
        return ans != []

class Is_writing(Filter):
    key = "is_writing"
    async def check(self, message: types.Message):
        adm = "SELECT * FROM finished WHERE user_id = %s AND writing = %s"
        val = (message.from_user.id, 1)
        ans = database.select(adm, val)
        return ans != []

class Is_super_admin(Filter):
    key = "is_super_admin"
    async def check(self, message: types.Message):
        adm = "SELECT admin_id FROM admins WHERE admin_id = %s AND super = %s"
        val = (message.from_user.id, 1)
        ans = database.select(adm, val)
        return ans != []
    
