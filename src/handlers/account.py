from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.interface.keyboards.account import account_options
from src.interface.keyboards.menu import menu_options
from src.interface.texts import menu_text
from src.services.user import UserService
from aiogram.filters import Command
from src.handlers.registration import start_registration

router = Router()


@router.message(Command("profile"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)

    user = await UserService.get_by_tg_id(tg_id)
    if user is None:
        await start_registration(message, state)

    else:

        profile_text = (
            f"*👤 Profile:*\n"
            f"*Name:* {user["username"]}\n"
            f"*NU ID:* {user["nu_id"] if user["nu_id"] else "n/a"}\n"
            f"*Gender:* {user["gender"]}\n"
            f"*Looking for:* {user["preference"]}\n"
            f"*Course:* {user["course"]}\n"
            f"*Description:* {user["description"]}\n"
        )
        await message.answer_photo(
            photo=user["photo_url"],
            caption=profile_text,
            parse_mode="Markdown",
            reply_markup=account_options
        )


# [InlineKeyboardButton(text="Anketa", callback_data="anketa")],
#     [InlineKeyboardButton(text="Change smth", callback_data="update_profile")],
#     [InlineKeyboardButton(text="Deactivate", callback_data="deactivate_profile")],
#     [InlineKeyboardButton(text="Menu", callback_data="menu")]
@router.callback_query(F.data == "menu")
async def get_full_profile(callback: CallbackQuery):
    await callback.message.answer(menu_text, reply_markup=menu_options)


@router.callback_query(F.data == "update_profile")
async def update_profile(callback: CallbackQuery):
    pass


@router.callback_query(F.data == "anketa")
async def update_profile(callback: CallbackQuery):
    pass


@router.callback_query(F.data == "deactivate_profile")
async def update_profile(callback: CallbackQuery):
    pass
