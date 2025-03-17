from src.database.postgres import get_postgres
from src.services.user import UserService
from src.dependencies.user_repo import get_user_repo
_user_service_instance = None  # Store a single instance


async def get_user_service() -> UserService:
    """Provides a singleton UserService instance."""
    global _user_service_instance
    if _user_service_instance is None:
        _user_service_instance = UserService(await get_user_repo())
    return _user_service_instance
