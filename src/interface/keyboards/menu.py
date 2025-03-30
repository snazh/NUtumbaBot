from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu_options = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="1 👀")],
    [KeyboardButton(text="2 👤")],
    [KeyboardButton(text="3 📜")],
    [KeyboardButton(text="4 📷")],
], resize_keyboard=True, one_time_keyboard=False)

proceed_activation = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="⚡ activate", callback_data="activate_profile")]

])
proceed_observe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🙂‍↕️ yes", callback_data="observe_lovers")]
])

profile_eval = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👍 Like", callback_data="like"),
     InlineKeyboardButton(text="👎 Skip", callback_data="skip"),
     InlineKeyboardButton(text="menu", callback_data="menu"), ]
])
