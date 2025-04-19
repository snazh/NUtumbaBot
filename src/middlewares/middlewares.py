from typing import Any, Callable, Dict, Awaitable, List
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.dependencies.service_di import get_user_service
from src.markups.keyboards.menu import proceed_activation, proceed_observe

from src.utils.message_formatter import get_formatted_anketa


class CustomMiddleware(BaseMiddleware):
    def __init__(self, skip_states: List[str]):
        self.skip_states = skip_states

    async def skip_handlers(self,
                            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                            event: TelegramObject,
                            data: Dict[str, Any]) -> None:
        state: FSMContext = data.get("state")
        current_state = await state.get_state()
        if state and current_state:
            if current_state.split(":")[0] in self.skip_states:
                return await handler(event, data)

        if isinstance(event, CallbackQuery) and event.data == "activate_profile":
            return await handler(event, data)


class CheckSearchStatusMiddleware(CustomMiddleware):

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:
        user_service = await get_user_service()

        tg_id = str(event.from_user.id)
        user = await user_service.get_profile(tg_id)
        data["user"] = user
        data["user_service"] = user_service
        await self.skip_handlers(handler, event, data)

        if user is None or (
                isinstance(event, Message) and event.text and event.text.startswith(("/register", "/start"))):
            return await handler(event, data)

        if not user["search_status"]:
            data["search_status"] = False
            if isinstance(event, CallbackQuery):
                await self._send_inactive_profile(event.message, user)
            else:
                await self._send_inactive_profile(event, user)
            return
        else:
            data["search_status"] = True

        return await handler(event, data)

    async def _send_inactive_profile(self, event: TelegramObject, user: Dict[str, Any]) -> None:

        user_text = get_formatted_anketa(user)
        await event.answer_photo(photo=user["photo_url"], caption=user_text, parse_mode="Markdown")
        await event.answer("Your profile is inactive. Activate it?", reply_markup=proceed_activation)


class CheckForUpdates(CustomMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:
        await self.skip_handlers(handler, event, data)

        user_service = await get_user_service()
        current_user = data["user"]
        lovers = await user_service.get_user_lovers(current_user["id"])

        if lovers:
            data["lovers"] = lovers
            if isinstance(event, CallbackQuery) and event.data == "observe_lovers":

                return await handler(event, data)
            else:
                await self._notify_user(event, lovers, current_user)
                return
        else:
            return await handler(event, data)

    async def _notify_user(self,
                           event: TelegramObject,
                           lovers: List[Dict[str, Any]],
                           user: Dict[str, Any]):
        new_event = event.message if isinstance(event, CallbackQuery) else event
        partners_num = len(lovers)
        notification = ""
        pronounce = ""
        match user["preference"]:
            case "male":
                notification = f"{partners_num} guy{"s" if partners_num > 1 else ""}"
                pronounce = "him"
            case "female":
                notification = f"{partners_num} girl{"s" if partners_num > 1 else ""} "
                pronounce = "her"
            case "both":
                notification = f"{partners_num} {"people" if partners_num > 1 else "person"}"
                pronounce = "them"
        await new_event.answer(f"You have {notification} who liked you. Wanna see {pronounce}",
                               reply_markup=proceed_observe)
