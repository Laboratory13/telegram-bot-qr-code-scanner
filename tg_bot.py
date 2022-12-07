from time import sleep
from aiogram import executor
from main import dp
import handlers


async def shutting(e):
    print("Shutting down!")


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=handlers.admin.startup,  skip_updates=True, on_shutdown=shutting, relax=0.3)
    except:
        print("Error in connection!")