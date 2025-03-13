import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from config import app_settings
from src.database.postgres import init_postgres, close_postgres
from src.handlers.registration import router as registration_router
from src.handlers.account import router as account_router

# Initialize bot and dispatcher
bot = Bot(token=app_settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(registration_router)
dp.include_router(account_router)
# Enable logging
logging.basicConfig(level=logging.INFO)


# Start command
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Hello! Welcome to the bot. Use /help to see commands.")


# Help command
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Available commands:\n/start - Welcome message\n/help - List commands")


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
