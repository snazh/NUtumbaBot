from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    username = State()
    age = State()
    course = State()
    photo = State()
    description = State()
    gender = State()
    preference = State()



class UpdateProfileState(StatesGroup):
    field = State()
    value = State()