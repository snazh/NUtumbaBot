from src.dependencies.service_di import get_user_service
from src.utils.message_formatter import get_formatted_anketa

from src.interface.keyboards.account import course, gender, preference, get_account_options
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


# Define User Registration States
class RegistrationState(StatesGroup):
    username = State()
    age = State()
    course = State()
    photo = State()
    description = State()
    gender = State()
    preference = State()


# Step 1: Start Registration
@router.message(Command("register"))
async def start_registration(message: Message, state: FSMContext):
    """Initiates the registration process."""
    user_service = await get_user_service()
    tg_id = str(message.from_user.id)
    user = await user_service.get_profile(tg_id)

    if user is None:
        await message.answer("📝 Please enter your username:")
        await state.set_state(RegistrationState.username)
    else:
        await message.answer("✅ You are already registered.")
        return


# Step 2: Capture Username
@router.message(RegistrationState.username)
async def process_username(message: Message, state: FSMContext):
    """Stores username and asks for age."""

    username = message.text.strip()

    if len(username) > 32:
        await message.answer("❌ Username is too long (max 32 characters). Try again.")
        return
    elif len(username) < 2:
        await message.answer("❌ Username is too short. Try again.")
        return

    await state.update_data(username=username)
    await message.answer("📅 Enter your age (e.g., 21):")
    await state.set_state(RegistrationState.age)


# Step 3: Capture Age
@router.message(RegistrationState.age)
async def process_age(message: Message, state: FSMContext):
    """Stores age and asks for course."""
    if not message.text.isdigit() or int(message.text) < 16 or int(message.text) > 100:
        await message.answer("❌ Please enter a valid age (must be from 16-100).")
        return

    await state.update_data(age=int(message.text))
    await message.answer("🎓 Select your course:", reply_markup=course)
    await state.set_state(RegistrationState.course)


# Step 4: Capture Course
@router.message(RegistrationState.course)
async def process_course(message: Message, state: FSMContext):
    """Stores course and asks for photo."""
    valid_courses = ["NUFYP", "Bachelor 1", "Bachelor 2", "Bachelor 3", "Bachelor 4", "Graduate", "PhD", "Other"]
    if message.text not in valid_courses:
        await message.answer("❌ Invalid course. Please select from the keyboard.")
        return

    await state.update_data(course=message.text)
    await message.answer("📸 Please send your profile photo:")
    await state.set_state(RegistrationState.photo)


# Step 5: Capture Photo
@router.message(RegistrationState.photo)
async def process_photo(message: Message, state: FSMContext):
    """Stores user photo and asks for description."""
    if not message.photo:
        await message.answer("❌ Please send a valid photo.")
        return
    photo = message.photo[-1]  # Get the highest resolution photo

    await state.update_data(photo_url=photo.file_id)
    await message.answer("📜 Enter a short description about yourself (max 2048 characters):")
    await state.set_state(RegistrationState.description)


# Step 6: Capture Description
@router.message(RegistrationState.description)
async def process_description(message: Message, state: FSMContext):
    """Stores description and asks for gender."""
    description = message.text.strip()
    if len(description) > 2048:
        await message.answer("❌ Description is too long. Try again (max 2048 characters).")
        return
    elif len(description) < 10:
        await message.answer("❌ Description is too short. Try again (at least 10 characters).")
        return

    await state.update_data(description=description)
    await message.answer("⚤ Select your gender:", reply_markup=gender)
    await state.set_state(RegistrationState.gender)


# Step 7: Capture Gender
@router.message(RegistrationState.gender)
async def process_gender(message: Message, state: FSMContext):
    """Stores gender and asks for soulmate preference."""
    valid_genders = ["male", "female", "other"]
    if message.text not in valid_genders:
        await message.answer("❌ Invalid selection. Please choose from the keyboard.1")
        return

    await state.update_data(gender=message.text)
    await message.answer("💕 Select your preferred soulmate gender:", reply_markup=preference)
    await state.set_state(RegistrationState.preference)


# Step 8: Capture Soulmate Gender
@router.message(RegistrationState.preference)
async def process_preference(message: Message, state: FSMContext):
    """Stores soulmate gender preference and finalizes registration."""
    valid_genders = ["male", "female", "both"]
    if message.text not in valid_genders:
        await message.answer("❌ Invalid selection. Please choose from the keyboard.")
        return

    user_data = await state.get_data()
    user_data["preference"] = message.text
    user_data["tg_id"] = str(message.from_user.id)

    user_service = await get_user_service()
    # Save user to DB

    result = await user_service.create_user(user_data)

    if result:

        await message.answer("✅ Registration complete! That how your anketa looks like")
        await message.answer_photo(
            photo=user_data["photo_url"],
            caption=get_formatted_anketa(user_data),
            parse_mode="Markdown",
            reply_markup=await get_account_options("anketa")
        )

    else:
        await message.answer("❌ Registration failed. Please try again.")

    # End FSM
    await state.clear()
