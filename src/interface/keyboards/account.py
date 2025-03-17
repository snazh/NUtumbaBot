from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

course = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="NUFYP")],
    [KeyboardButton(text="Bachelor 1")],
    [KeyboardButton(text="Bachelor 2")],
    [KeyboardButton(text="Bachelor 3")],
    [KeyboardButton(text="Bachelor 4")],
    [KeyboardButton(text="Graduate")],
    [KeyboardButton(text="PhD")],
    [KeyboardButton(text="Other")]], resize_keyboard=True)

gender = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="male")],
    [KeyboardButton(text="female")],
    [KeyboardButton(text="other")],
], resize_keyboard=True)
preference = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="male")],
    [KeyboardButton(text="female")],
    [KeyboardButton(text="both")],
], resize_keyboard=True)


async def get_account_options(profile_type: str):
    profile_text = "Profile details" if profile_type == "profile_details" else "Anketa"
    profile_callback = "full_profile" if profile_type == "profile_details" else "anketa"
    return InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text=profile_text, callback_data=profile_callback)],
        [InlineKeyboardButton(text="Change smth", callback_data="update_profile")],
        [InlineKeyboardButton(text="Deactivate", callback_data="deactivate_profile")],
        [InlineKeyboardButton(text="Menu", callback_data="menu")]
    ])


update_options = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="username", callback_data="username")],
    [InlineKeyboardButton(text="photo", callback_data="photo_url")],
    [InlineKeyboardButton(text="description", callback_data="description")],

])
