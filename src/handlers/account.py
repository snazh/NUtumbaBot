from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.dependencies.service_di import get_user_service
from src.interface.keyboards.account import get_account_options, update_options
from src.interface.keyboards.menu import menu_options, proceed_activation
from src.interface.texts import menu_text
from src.utils.message_formatter import get_formatted_profile, get_formatted_anketa
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("profile"))
async def get_anketa(message: Message, user: dict):
    keyboard = await get_account_options("profile_details")
    await message.answer_photo(
        photo=user["photo_url"],
        caption=get_formatted_anketa(user),
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "menu")
async def get_menu(callback: CallbackQuery):
    await callback.message.answer(menu_text.actions, reply_markup=menu_options)


@router.callback_query(F.data == "deactivate_profile")
async def deactivate_account(callback: CallbackQuery):

    user_service = await get_user_service()
    user_id = str(callback.from_user.id)
    if await user_service.change_status(user_id, False):
        await callback.message.answer(f"✅ Your profile deactivated")
    else:
        await callback.message.answer("❌ Deactivation failed.")


@router.callback_query(F.data == "activate_profile")
async def activate_account(callback: CallbackQuery):
    user_service = await get_user_service()
    user_id = str(callback.from_user.id)
    if await user_service.change_status(user_id, True):
        await callback.message.answer(f"✅ Your profile activated")
    else:
        await callback.message.answer("❌ Activation failed.")


@router.callback_query(F.data == "full_profile")
async def get_full_profile(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    user_service = await get_user_service()
    user = await user_service.get_profile(user_id)
    keyboard = await get_account_options("anketa")
    await callback.message.answer_photo(
        photo=user["photo_url"],
        caption=get_formatted_profile(user),
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "anketa")
async def get_anketa(callback: CallbackQuery):
    user_service = await get_user_service()
    user_id = str(callback.from_user.id)
    user = await user_service.get_profile(user_id)
    keyboard = await get_account_options("profile_details")
    await callback.message.answer_photo(
        photo=user["photo_url"],
        caption=get_formatted_anketa(user),
        parse_mode="Markdown",
        reply_markup=keyboard
    )


class UpdateProfileState(StatesGroup):
    field = State()
    value = State()


@router.callback_query(F.data == "update_profile")
async def get_update_options(callback: CallbackQuery, state: FSMContext):
    """Ask for field"""
    await callback.message.answer("What do you want to update?", reply_markup=update_options)
    await state.set_state(UpdateProfileState.field)


@router.callback_query(F.data.in_(["username", "description", "photo"]))
async def handle_field_selection(callback: CallbackQuery, state: FSMContext):
    """Store selected field and ask for new value."""
    field = callback.data
    await state.update_data(field=field)
    await callback.message.answer(f"Enter your new {field.replace('_', ' ')}:")
    await state.set_state(UpdateProfileState.value)


@router.message(UpdateProfileState.value)
async def update_value(message: Message, state: FSMContext):
    """Save new value and update profile."""
    user_service = await get_user_service()
    user_id = str(message.from_user.id)
    data = await state.get_data()

    result = None
    match data["field"]:
        case "username":
            result = await user_service.update_username(tg_id=user_id, new_name=message.text)

        case "description":
            result = await user_service.update_description(tg_id=user_id, new_desc=message.text)
        case "description":
            result = await user_service.update_photo(tg_id=user_id, new_photo=message.photo[-1].file_id)

    if result:
        await message.answer(f"✅ Your {data['field'].replace('_', ' ')} has been updated!")
    else:
        await message.answer("❌ Update failed.")

    await state.clear()


@router.callback_query(F.data == "observe_lovers")
async def observe_lovers(callback: CallbackQuery, state: FSMContext):
    pass