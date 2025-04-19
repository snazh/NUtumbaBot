from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.helpers.user import show_profile
from src.states.search import ObserveState
from src.dependencies.service_di import get_eval_service, get_relationship_service

from src.markups.keyboards.menu import get_eval_keyboard

router = Router()


@router.callback_query(F.data == "observe_lovers")
async def observe_lovers(callback: CallbackQuery, state: FSMContext, lovers: List[dict]):
    if not lovers:
        await callback.message.answer("❌ No lovers found right now.")
        return
    await state.update_data(lovers=lovers, index=0)
    await state.set_state(ObserveState.index)
    await show_profile(callback.message, profiles=lovers, index=0, keyboard=get_eval_keyboard(goal="observe"))


@router.callback_query(F.data.in_({"mutual_like", "refuse"}))
async def handle_reaction_reply(callback: CallbackQuery, state: FSMContext, user: dict):
    eval_service = await get_eval_service()
    relationship_service = await get_relationship_service()
    data = await state.get_data()
    profiles = data.get("lovers")
    index = data.get("index", 0)

    current_profile = profiles[index]

    relationship_data = {
        "user1": current_profile["id"],
        "user2": user["id"],
        "status": "blacklist"
    }

    if callback.data == "mutual_like":
        relationship_data["status"] = "couple"
        mention = f'<a href="tg://user?id={current_profile["tg_id"]}">Click to open user</a>'
        await callback.message.answer(mention, parse_mode="HTML")

    await eval_service.delete_eval(user["id"])
    await relationship_service.create_relationship(relationship_data)
    # Show next profile
    if index + 1 < len(profiles):
        await state.update_data(index=index + 1)
        await show_profile(callback.message, profiles, index + 1, keyboard=get_eval_keyboard(goal="observe"))
    else:
        await callback.message.answer("🎉 You've reached the end of the profiles!")
        await state.clear()
