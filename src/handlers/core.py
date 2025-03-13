from typing import Optional

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.interface.texts import commands, menu_options
from src.services.user import UserService
from src.handlers.registration import start_registration
from src.interface.keyboards.menu import menu_options
from src.interface.texts import menu_text

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    user = await UserService.get_by_tg_id(tg_id)
    if user is None:
        await start_registration(message, state)

    else:
        await cmd_menu(message)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(commands.help)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(menu_text, reply_markup=menu_options)

# async def redirect_to_register(message: Message, state: FSMContext) -> Optional[bool]:
#     tg_id = str(message.from_user.id)
#     user = await UserService.get_by_tg_id(tg_id)
#
#     if user is None:
#         await start_registration(message, state)
#
#     else:
#         return True
