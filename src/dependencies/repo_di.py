from src.database.postgres import get_postgres
from src.repository.evaluation import EvalRepository
from src.repository.user import UserRepository
from src.repository.relationship import RelationshipRepository

_user_repo_instance = None  # Store a single instance


async def get_user_repo() -> UserRepository:
    """Provides a singleton UserService instance."""
    global _user_repo_instance
    if _user_repo_instance is None:
        pool = await get_postgres()
        _user_repo_instance = UserRepository(db_pool=pool, table="user",
                                             columns=["username", "nu_id", "description", "photo_url", "search_status"])
    return _user_repo_instance


_eval_repo_instance = None


async def get_eval_repo() -> EvalRepository:
    """Provides a singleton UserService instance."""
    global _eval_repo_instance
    if _eval_repo_instance is None:
        pool = await get_postgres()
        _eval_repo_instance = EvalRepository(db_pool=pool, table="evaluation",
                                             columns=["anketa_id", "lover_id", "evaluation"])
    return _eval_repo_instance


_relationship_repo_instance = None


async def get_relationship_repo() -> RelationshipRepository:
    """Provides a singleton UserService instance."""
    global _relationship_repo_instance
    if _relationship_repo_instance is None:
        pool = await get_postgres()
        _relationship_repo_instance = RelationshipRepository(db_pool=pool, table="relationship",
                                                             columns=["user1", "user2", "status", "startDate"])
    return _relationship_repo_instance
