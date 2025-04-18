from aiogram.types import Message


from src.utils.message_formatter import get_formatted_anketa


async def show_profile(message: Message, profiles: list, index: int, keyboard):
    profile = profiles[index]

    anketa_text = get_formatted_anketa(profile)

    await message.answer_photo(
        photo=profile["photo_url"],
        caption=anketa_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
