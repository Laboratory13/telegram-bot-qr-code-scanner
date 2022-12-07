from aiogram.dispatcher.filters import Filter
from aiogram import types
from helpers.self_connection import check_admin, check_has_tel, check_has_status, get_user_phone, calc_update, register_db, check_user
import helpers.joha_api as japi

class Is_admin( Filter ):
    key = "is_admin"
    async def check( self, message: types.Message ):
        return check_admin( message.from_user.id )

class Is_user( Filter ):
    key = "is_user"
    async def check(self, message: types.Message ):
        return check_user( message.from_user.id )

class Share_tel( Filter ):
    key = "share_tel"
    async def check( self, message: types.Message ):
        return not check_has_tel( message.from_user.id )

class Have_status( Filter ):
    key = "have_status"
    async def check( self, message: types.Message ):
        return check_has_status( message.from_user.id )

class Not_allowed( Filter ):
    key = "not_allowed"
    async def check( self, message: types.Message ):
        phone = get_user_phone( message.from_user.id )
        if calc_update( message.from_user.id ):
            reg_res = japi.register( phone, message.from_user.id )
            if "user" in reg_res:
                register_db( message.from_user.id, message.from_user.full_name, phone, reg_res )
                return False
            else:
                return True
        else:
            return False