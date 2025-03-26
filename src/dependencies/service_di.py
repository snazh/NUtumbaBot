from src.database.postgres import get_postgres
from src.services.evaluation import EvalService
from src.services.user import UserService
from src.dependencies.repo_di import get_user_repo, get_eval_repo

_user_service_instance = None  # Store a single instance


async def get_user_service() -> UserService:
    """Provides a singleton UserService instance."""
    global _user_service_instance
    if _user_service_instance is None:
        _user_service_instance = UserService(await get_user_repo())
    return _user_service_instance


_eval_service_instance = None


async def get_eval_service() -> EvalService:
    """Provides a singleton UserService instance."""
    global _eval_service_instance
    if _eval_service_instance is None:
        _eval_service_instance = EvalService(await get_eval_repo())
    return _eval_service_instance
