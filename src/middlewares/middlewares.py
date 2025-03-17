import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message

from src.dependencies.user_service import get_user_service
from src.interface.keyboards.menu import menu_options, proceed_activation

from src.utils.message_formatter import get_formatted_anketa
from aiogram.filters import CommandStart

class CheckSearchStatusMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:

        if isinstance(event, Message) and event.text and event.text.startswith(("/start", "/register")):
            return await handler(event, data)

        # ✅ Ignore messages if user is in a registration state
        state: FSMContext = data.get("state")  # Get FSM state
        current_state = await state.get_state()  # Get current state name

        if current_state and current_state.startswith("RegistrationState"):
            return await handler(event, data)  # Skip middleware processing

        user_service = await get_user_service()
        user_id = str(event.from_user.id)
        user = await user_service.get_profile(user_id)
        print(user_id, user)

        if not user["search_status"]:
            data["search_status"] = False
            await event.answer_photo(
                photo=user["photo_url"],
                caption=get_formatted_anketa(user),
                parse_mode="Markdown"
            )
            await event.answer("Your profile not active. Wanna recover your anketa?", reply_markup=proceed_activation)

            return
        else:
            data["search_status"] = True
        return await handler(event, data)
