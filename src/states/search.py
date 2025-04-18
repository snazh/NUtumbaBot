from aiogram.fsm.state import StatesGroup, State


class SearchState(StatesGroup):
    index = State()  # current profile index
    profiles = State()  # list of profiles (stored in-memory for the session)\


class ObserveState(StatesGroup):
    index = State()
    lovers = State()
