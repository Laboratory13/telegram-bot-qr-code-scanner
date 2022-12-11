from main import dp, bot
import handlers



from aiogram.utils.executor import start_webhook



# webhook settings
WEBHOOK_HOST = 'https://bot.pharmiq.uz'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8000



async def startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start
    print("Successfuly started webhook telegram bot!")


async def shutting(dp):
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    print("Shuting down successfuly removed webhook.")


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=startup,
        on_shutdown=shutting,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )