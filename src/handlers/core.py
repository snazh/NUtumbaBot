from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.dependencies.service_di import get_user_service
from src.handlers.registration import start_registration
from src.interface.keyboards.menu import menu_options, proceed_activation
from src.interface.texts import menu_text, commands

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user: dict):

    if user is None:
        await message.answer("Welcome to NUtinder bot. Lets create your first anketa")
        await start_registration(message, state)
        return

    await message.answer(menu_text.actions, reply_markup=menu_options)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(commands.help)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(menu_text.actions, reply_markup=menu_options)


