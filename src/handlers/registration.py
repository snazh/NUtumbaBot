from src.schemas.user import UserCreate
from src.services.user import UserService
from src.interface.keyboards.account import course, gender, preference
from aiogram import Router, types, F
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
async def start_registration(message: types.Message, state: FSMContext):
    """Initiates the registration process."""
    tg_id = str(message.from_user.id)
    user = await UserService.get_by_tg_id(tg_id)

    if user is None:
        await message.answer("📝 Please enter your username:")
        await state.set_state(RegistrationState.username)
    else:
        await message.answer("✅ You are already registered.")
        return


# Step 2: Capture Username
@router.message(RegistrationState.username)
async def process_username(message: types.Message, state: FSMContext):
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
async def process_age(message: types.Message, state: FSMContext):
    """Stores age and asks for course."""
    if not message.text.isdigit() or int(message.text) < 16:
        await message.answer("❌ Please enter a valid age (must be 16 or older).")
        return

    await state.update_data(age=int(message.text))
    await message.answer("🎓 Select your course:", reply_markup=course)
    await state.set_state(RegistrationState.course)


# Step 4: Capture Course
@router.message(RegistrationState.course)
async def process_course(message: types.Message, state: FSMContext):
    """Stores course and asks for photo."""
    valid_courses = ["NUFYP", "Bachelor 1", "Bachelor 2", "Bachelor 3", "Bachelor 4", "Graduate", "PhD", "Other"]
    if message.text not in valid_courses:
        await message.answer("❌ Invalid course. Please select from the keyboard.")
        return

    await state.update_data(course=message.text)
    await message.answer("📸 Please send your profile photo:")
    await state.set_state(RegistrationState.photo)


# Step 5: Capture Photo
@router.message(RegistrationState.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    """Stores user photo and asks for description."""
    photo = message.photo[-1]  # Get the highest resolution photo
    if not photo:
        await message.answer("❌ Please send a valid photo.")
        return

    await state.update_data(photo_url=photo.file_id)
    await message.answer("📜 Enter a short description about yourself (max 2048 characters):")
    await state.set_state(RegistrationState.description)


# Step 6: Capture Description
@router.message(RegistrationState.description)
async def process_description(message: types.Message, state: FSMContext):
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
async def process_gender(message: types.Message, state: FSMContext):
    """Stores gender and asks for soulmate preference."""
    valid_genders = ["male", "female", "other"]
    if message.text not in valid_genders:
        await message.answer("❌ Invalid selection. Please choose from the keyboard.")
        return

    await state.update_data(gender=message.text)
    await message.answer("💕 Select your preferred soulmate gender:", reply_markup=preference)
    await state.set_state(RegistrationState.preference)


# Step 8: Capture Soulmate Gender
@router.message(RegistrationState.preference)
async def process_preference(message: types.Message, state: FSMContext):
    """Stores soulmate gender preference and finalizes registration."""
    valid_genders = ["male", "female", "both"]
    if message.text not in valid_genders:
        await message.answer("❌ Invalid selection. Please choose from the keyboard.")
        return

    user_data = await state.get_data()
    user_data["preference"] = message.text
    tg_id = str(message.from_user.id)

    # Save user to DB
    new_user = UserCreate(
        username=user_data["username"],
        tg_id=tg_id,
        age=user_data["age"],
        course=user_data["course"],
        description=user_data["description"],
        gender=user_data["gender"],
        preference=user_data["preference"],
        photo_url=user_data["photo_url"],
        nu_id=None  # Optional
    )

    result = await UserService.insert(new_user)

    if result:
        await message.answer("✅ Registration complete! You can now use other bot features.")
    else:
        await message.answer("❌ Registration failed. Please try again.")

    # Ensure the database reflects the user is now registered
    saved_user = await UserService.get_by_tg_id(tg_id)
    if saved_user:
        await message.answer("✅ Your data is saved in the system.")
    else:
        await message.answer("⚠️ Warning: Your registration might not have been saved properly.")

    # End FSM
    await state.clear()
