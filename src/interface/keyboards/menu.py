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


def get_eval_keyboard(goal: str):
    like_callback = ""
    skip_callback = ""
    match goal:

        case "search":
            like_callback = "like"
            skip_callback = "skip"
        case "observe":
            like_callback = "mutual_like"
            skip_callback = "refuse"

    profile_eval = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👍 Like", callback_data=like_callback),
         InlineKeyboardButton(text="👎 Skip", callback_data=skip_callback),
         InlineKeyboardButton(text="menu", callback_data="menu"), ]
    ])

    return profile_eval
