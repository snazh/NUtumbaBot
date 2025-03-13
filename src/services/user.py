from typing import Optional

from src.database.postgres import get_postgres
from src.schemas.user import UserUpdate, UserCreate
from loguru import logger


class UserService:
    @staticmethod
    async def insert(user: UserCreate) -> bool:
        """Insert a new user"""
        pool = await get_postgres()
        async with pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO users "
                    "(username, tg_id, nu_id, age, course, description, photo_url, gender, preference)"
                    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9 )",
                    user.username, user.tg_id, user.nu_id, user.age, user.course, user.description, user.photo_url,
                    user.gender, user.preference
                )
                return True
            except Exception as e:
                logger.error(f"❌ Failed to register user {user.tg_id}: {e}")
                return False

    @staticmethod
    async def get_by_tg_id(tg_id: str) -> Optional[dict]:
        """Fetch user by tg_id"""
        pool = await get_postgres()
        async with pool.acquire() as conn:
            try:
                user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
                if user:
                    return dict(user)
                return None
            except Exception as e:
                logger.error(f"❌ Failed to fetch user with tg_id({tg_id}): {e}")
                return None

    # @staticmethod
    # async def update(tg_id: str, user: UserUpdate) -> Optional[dict]:
    #     """Update user"""
    #     pool = await get_postgres()
    #     async with pool.acquire() as conn:
    #         try:
    #             result = await conn.execute(
    #                 "UPDATE users"
    #                 "SET ",
    #                 user.username, user.tg_id, user.nu_id, user.age, user.course, user.description
    #             )
    #             return result
    #         except Exception as e:
    #             logger.error(f"❌ Failed to update user {tg_id}: {e}")
    #             return None

    @staticmethod
    async def delete(tg_id: str) -> bool:
        """Delete a user by tg_id"""
        pool = await get_postgres()
        async with pool.acquire() as conn:
            result = await conn.execute("DELETE FROM users WHERE tg_id = $1", tg_id)
            if result == "DELETE 1":
                logger.info(f"🗑️ User with tg_id {tg_id} deleted.")
                return True
            return False
