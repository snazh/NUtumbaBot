from typing import List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.handlers.user_actions.account import get_anketa
from src.helpers.user import show_profile
from src.services.user import UserService
from src.states.search import SearchState, ObserveState

from src.dependencies.service_di import get_user_service, get_eval_service
from src.interface.keyboards.menu import get_eval_keyboard, proceed_observe

router = Router()

@router.message(Command("test"))
async def gay(message: Message):
    await message.answer("hello", reply_markup=proceed_observe)


@router.callback_query(F.data == "observe_lovers")
async def observe_lovers(callback: CallbackQuery, state: FSMContext, lovers: List[dict]):
    print("observe_lovers handler triggered")  # Debugging
    print("Lovers received:", lovers)
    if not lovers:
        await callback.message.answer("❌ No lovers found right now.")
        return
    await state.update_data(lovers=lovers, index=0)
    await state.set_state(ObserveState.index)
    await show_profile(callback.message, profiles=lovers, index=0, keyboard=get_eval_keyboard(goal="observe"))


@router.callback_query(F.data.in_({"mutual_like", "refuse"}))
async def handle_reaction(callback: CallbackQuery, state: FSMContext, user: dict):
    eval_service = await get_eval_service()

    data = await state.get_data()
    profiles = data.get("profiles")
    index = data.get("index", 0)

    current_profile = profiles[index]

    eval_data = {

        "anketa_id": current_profile["id"],
        "lover_id": user["id"],
        "evaluation": False
    }
    if callback.data == "like":
        eval_data["evaluation"] = True

    await eval_service.eval_profile(eval_data)

    # Show next profile
    if index + 1 < len(profiles):
        await state.update_data(index=index + 1)
        await show_profile(callback.message, profiles, index + 1)
    else:
        await callback.message.answer("🎉 You've reached the end of the profiles!")
        await state.clear()

@router.message(F.text.startswith("1"))
async def menu_search_anketas(message: Message, state: FSMContext, user: dict, user_service: UserService):

    profiles = await user_service.get_profile_list_for_user(user["id"])
    print(profiles)
    if not profiles:
        await message.answer("❌ No profiles found right now.")
        return
    await state.update_data(profiles=profiles, index=0)
    await state.set_state(SearchState.index)
    await show_profile(message, profiles=profiles, index=0, keyboard=get_eval_keyboard(goal="search"))


@router.callback_query(F.data.in_({"like", "skip"}))
async def handle_reaction(callback: CallbackQuery, state: FSMContext, user: dict):
    eval_service = await get_eval_service()

    data = await state.get_data()
    profiles = data.get("profiles")
    index = data.get("index", 0)

    current_profile = profiles[index]

    eval_data = {

        "anketa_id": current_profile["id"],
        "lover_id": user["id"],
        "evaluation": False
    }
    if callback.data == "like":
        eval_data["evaluation"] = True

    await eval_service.eval_profile(eval_data)

    # Show next profile
    if index + 1 < len(profiles):
        await state.update_data(index=index + 1)
        await show_profile(callback.message, profiles, index + 1, keyboard=get_eval_keyboard(goal="search"))
    else:
        await callback.message.answer("🎉 You've reached the end of the profiles!")
        await state.clear()


@router.message(F.text.startswith("2"))
async def menu_profile(message, user: dict):
    await get_anketa(message, user)
    return
