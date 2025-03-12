from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from loguru import logger

from src.schemas.user import UserCreate
from src.services.user import UserService

router = Router()


@router.message(Command("register"))
async def register_handler(message: Message):
    """Register a new user"""
    tg_id = str(message.from_user.id)

    user_data = UserCreate(
        username="Sanzhar",
        tg_id=tg_id,
        nu_id=None,  # Optional
        age=18,  # Default age (can be updated later)
        course="NUFYP",  # Default course (Change accordingly)
        description="New user"
    )

    success = await UserService.insert(user_data)

    if success:
        await message.answer(f"✅ User {1} registered successfully!")
    else:
        await message.answer("❌ Registration failed. Please try again.")
