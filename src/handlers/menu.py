

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from src.utils.message_formatter import get_formatted_anketa
from src.dependencies.service_di import get_user_service, get_eval_service

from src.interface.keyboards.menu import profile_eval


router = Router()


class SearchState(StatesGroup):
    index = State()  # current profile index
    profiles = State()  # list of profiles (stored in-memory for the session)


async def show_profile(message: Message, profiles: list, index: int):
    profile = profiles[index]

    anketa_text = get_formatted_anketa(profile)

    await message.answer_photo(
        photo=profile["photo_url"],
        caption=anketa_text,
        parse_mode="Markdown",
        reply_markup=profile_eval
    )


@router.message(F.text.startswith("1"))
async def menu_search_anketas(message: Message, state: FSMContext):
    user_service = await get_user_service()
    user_id = str(message.from_user.id)
    profiles = await user_service.get_profile_list_for_user(user_id)

    if not profiles:
        await message.answer("❌ No profiles found right now.")
        return
    await state.update_data(profiles=profiles, index=0)
    await state.set_state(SearchState.index)
    await show_profile(message, profiles, 0)


@router.callback_query(F.data.in_({"like", "skip"}))
async def handle_reaction(callback: CallbackQuery, state: FSMContext):
    eval_service = await get_eval_service()
    user_service = await get_user_service()
    data = await state.get_data()
    profiles = data.get("profiles")
    index = data.get("index", 0)

    current_profile = profiles[index]
    user_id = (await user_service.get_profile(str(callback.from_user.id)))["id"]

    eval_data = {

        "anketa_id": current_profile["id"],
        "lover_id": user_id,
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


