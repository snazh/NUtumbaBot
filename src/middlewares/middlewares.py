import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.dependencies.service_di import get_user_service
from src.interface.keyboards.menu import menu_options, proceed_activation

from src.utils.message_formatter import get_formatted_anketa
from aiogram.filters import CommandStart
from src.handlers.registration import start_registration


class CheckSearchStatusMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:
        user_service = await get_user_service()
        user_id = str(event.from_user.id)
        user = await user_service.get_profile(user_id)
        data["user"] = user
        if user is None:
            return await handler(event, data)

        if isinstance(event, Message) and event.text and event.text.startswith(("/register", "/start")):
            return await handler(event, data)

        # ✅ Ignore messages if user is in a registration state
        state: FSMContext = data.get("state")  # Get FSM state
        current_state = await state.get_state()  # Get current state name

        if current_state and current_state.startswith("RegistrationState"):
            return await handler(event, data)  # Skip middleware processing

        if not user["search_status"]:
            data["search_status"] = False
            user_text = get_formatted_anketa(user)

            await event.answer_photo(photo=user["photo_url"], caption=user_text, parse_mode="Markdown")
            await event.answer("Your profile is not active. Wanna recover your anketa?",
                               reply_markup=proceed_activation)

            return
        else:
            data["search_status"] = True
        return await handler(event, data)


class CheckForUpdates(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:

        if isinstance(event, Message) and event.text and event.text.startswith(("/register")):
            return await handler(event, data)

        # ✅ Ignore messages if user is in a registration state
        state: FSMContext = data.get("state")  # Get FSM state
        current_state = await state.get_state()  # Get current state name

        if current_state and current_state.startswith("RegistrationState"):
            return await handler(event, data)  # Skip middleware processing

        user_service = await get_user_service()

        user_id = str(event.from_user.id)
        partners = await user_service.get_user_who_liked_user(user_id)
        current_user = await user_service.get_profile(user_id)

        if not partners:
            return await handler(event, data)  # Skip middleware processing

        partner_num = len(partners)
        notification = ""
        pronounce = ""
        match current_user["preference"]:
            case "male":
                notification = f"{partner_num} guy{"s" if partner_num > 1 else ""}"
                pronounce = "him"
            case "female":
                notification = f"{partner_num} girl{"s" if partner_num > 1 else ""} "
                pronounce = "her"
            case "both":
                notification = f"{partner_num} {"people" if partner_num > 1 else "person"}"
                pronounce = "them"
        await event.answer(
            f"You have {notification} who liked you. Wanna see {pronounce}")
