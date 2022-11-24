
from helpers.filter import Is_admin
from aiogram import Bot, Dispatcher

# API_TOKEN = '5869984480:AAFtmMayAt7qdkWGCtaNyovORNKT0P1h0zQ'
API_TOKEN = '477383024:AAGgsYy0rOzQ7REfVPrZOWoKy1sv9LDXyK0'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.bind_filter(Is_admin)