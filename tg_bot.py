from time import sleep
from aiogram import executor
from main import dp
import handlers

async def shutting(e):
    print("Shutting down!")

async def startup(e):
    print("Bot is running...")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=startup, on_shutdown=shutting)