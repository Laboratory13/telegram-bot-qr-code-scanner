from aiogram.dispatcher.filters import Filter
from aiogram import types
from database.database import database

class Is_admin(Filter):
    key = "is_admin"
    async def check(self, message: types.Message):
        adm = "SELECT id FROM users WHERE id = %s AND is_admin = %s"
        val = (message.from_user.id, 1)
        ans = database.select_one(adm, val)      
        return ans != {}

class Share_tel(Filter):
    key = "share_tel"
    async def check(self, message: types.Message) -> bool:
        quer = "SELECT * FROM users WHERE id = %s"
        val = (message.from_user.id, )
        ans = database.select_one(quer, val)
        if ans == {}:
            return True
        else:
            return ans["tel"] == ""

class Have_status(Filter):
    key = "have_status"
    async def check(self, message: types.Message) -> bool:
        quer = "SELECT * FROM users WHERE id = %s"
        val = (message.from_user.id, )
        ans = database.select_one(quer, val)
        if ans == {}:
            return False
        else:
            return ans["status"] != 0