import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from src.dependencies.user_service import get_user_service
from src.interface.keyboards.menu import menu_options, proceed_activation

from src.utils.message_formatter import get_formatted_anketa


class CheckSearchStatusMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:

        print(isinstance(event, Message))
        user_service = await get_user_service()
        user_id = str(event.from_user.id)
        user = await user_service.get_profile(user_id)

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
