from src.dependencies.user_repo import get_user_repo
from src.repository.user import UserRepository
from src.schemas.user import UserCreate


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @classmethod
    async def create(cls):
        """Asynchronous constructor to create an instance of UserService"""
        user_repo = await get_user_repo()
        return cls(user_repo)

    async def create_user(self, user_data: dict):
        new_user = UserCreate(
            username=user_data["username"],
            tg_id=user_data["tg_id"],
            age=user_data["age"],
            course=user_data["course"],
            description=user_data["description"],
            gender=user_data["gender"],
            preference=user_data["preference"],
            photo_url=user_data["photo_url"],
            nu_id=None  # Optional
        )
        return await self.user_repo.insert(new_user)

    async def get_profile(self, tg_id: str):
        return await self.user_repo.get_by_tg_id(tg_id)

    async def update_username(self, tg_id: str, new_name: str) -> bool:
        return await self.user_repo.partial_update(tg_id=tg_id, parameter="username", value=new_name)

    async def update_description(self, tg_id: str, new_desc: str) -> bool:
        return await self.user_repo.partial_update(tg_id=tg_id, parameter="description", value=new_desc)

    async def update_photo(self, tg_id: str, new_photo: str) -> bool:
        return await self.user_repo.partial_update(tg_id=tg_id, parameter="photo", value=new_photo)

    async def change_status(self, tg_id: str, status: bool):
        return await self.user_repo.partial_update(tg_id=tg_id, parameter="search_status", value=status)
