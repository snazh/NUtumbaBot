from src.database.postgres import get_postgres
from src.repository.user import UserRepository

_user_repo_instance = None  # Store a single instance


async def get_user_repo() -> UserRepository:
    """Provides a singleton UserService instance."""
    global _user_repo_instance
    if _user_repo_instance is None:
        pool = await get_postgres()
        _user_repo_instance = UserRepository(pool)
    return _user_repo_instance
