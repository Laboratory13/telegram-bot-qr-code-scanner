
from helpers.filter import Is_admin
from aiogram import Bot, Dispatcher

# API_TOKEN = '5867243559:AAE9FtL9Hxrpy2geAsWNLB70Zz__CbJB-EM' # Bositkhon's bot
# API_TOKEN = '5869984480:AAFtmMayAt7qdkWGCtaNyovORNKT0P1h0zQ'
API_TOKEN = '477383024:AAE33xFWSas6jRROncgrsVOacJrrsDtHCkI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.bind_filter(Is_admin)