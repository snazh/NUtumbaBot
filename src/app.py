import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import app_settings
from src.database.postgres import init_postgres, close_postgres
from src.handlers.user_actions.registration import router as registration_router
from src.handlers.user_actions.account import router as account_router
from src.handlers.core import router as core_router
from src.middlewares.middlewares import CheckSearchStatusMiddleware, CheckForUpdates
from src.handlers.user_actions.menu import router as menu_router
from src.handlers.user_actions.soulmate import router as soulmate_router

# Initialize bot and dispatcher
bot = Bot(token=app_settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(soulmate_router)
dp.include_router(registration_router)
dp.include_router(account_router)
dp.include_router(core_router)
dp.include_router(menu_router)

dp.message.middleware.register(CheckSearchStatusMiddleware())
dp.callback_query.middleware.register(CheckSearchStatusMiddleware())
update_middleware = CheckForUpdates(skip_states=["RegistrationState", "ObserveState", "SearchState", "UpdateState"])
dp.message.middleware.register(update_middleware)
dp.callback_query.middleware.register(update_middleware)

# Enable logging
logging.basicConfig(level=logging.INFO)


# Main function to run the bot
async def main():
    """Start the bot with PostgreSQL connection."""
    logging.basicConfig(level=logging.INFO)

    await init_postgres()  # Initialize DB connection
    try:
        print("🚀 Bot is running...")
        await dp.start_polling(bot)
    finally:
        await close_postgres()  # Close DB connection on shutdown


if __name__ == "__main__":
    asyncio.run(main())
