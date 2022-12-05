from aiogram.dispatcher.filters import Filter
from aiogram import types
from helpers.self_connection import check_admin, check_has_tel, check_has_status

class Is_admin( Filter ):
    key = "is_admin"
    async def check( self, message: types.Message ):
        return check_admin( message.from_user.id )

class Share_tel( Filter ):
    key = "share_tel"
    async def check( self, message: types.Message ) -> bool:
        return not check_has_tel( message.from_user.id )

class Have_status( Filter ):
    key = "have_status"
    async def check( self, message: types.Message ) -> bool:
        check_has_status( message.from_user.id )