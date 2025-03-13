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

account_options = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="Anketa", callback_data="anketa")],
    [InlineKeyboardButton(text="Change smth", callback_data="update_profile")],
    [InlineKeyboardButton(text="Deactivate", callback_data="deactivate_profile")],
    [InlineKeyboardButton(text="Menu", callback_data="menu")]
])
