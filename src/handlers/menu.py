from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.dependencies.user_service import get_user_service
from src.handlers.registration import start_registration
from src.interface.keyboards.menu import menu_options, proceed_activation
from src.interface.texts import menu_text, commands

router = Router()


@router.message(lambda message: message.text == "1 👁️")
async def menu_search_anketas():
    pass
