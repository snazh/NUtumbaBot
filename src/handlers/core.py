from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.handlers.user_actions.registration import start_registration
from src.markups.keyboards.menu import menu_options
from src.markups.texts import menu_text, commands
from src.services.user import UserService

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user: dict, user_service: UserService):
    if user is None:
        await message.answer("Welcome to NUtinder bot. Lets create your first anketa")
        await start_registration(message, state, user_service=user_service)
        return

    await message.answer(menu_text.actions, reply_markup=menu_options)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(commands.help)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(menu_text.actions, reply_markup=menu_options)
