from typing import Optional
from loguru import logger
from src.repository.schemas.user import UserCreate
from src.repository.base import BaseRepo


class UserRepository(BaseRepo):

    async def insert(self, user: UserCreate) -> bool:
        """Insert a new user"""
        async with self.db_pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO users "
                    "(username, tg_id, nu_id, age, course, description, photo_url, gender, preference) "
                    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)",
                    user.username, user.tg_id, user.nu_id, user.age, user.course, user.description,
                    user.photo_url, user.gender, user.preference
                )
                return True
            except Exception as e:
                logger.error(f"❌ Failed to register user {user.tg_id}: {e}")
                return False

    async def get_by_tg_id(self, tg_id: str) -> Optional[dict]:
        """Fetch user by tg_id"""
        async with self.db_pool.acquire() as conn:
            try:
                user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
                return dict(user) if user else None
            except Exception as e:
                logger.error(f"❌ Failed to fetch user with tg_id({tg_id}): {e}")
                return None

    async def partial_update(self, tg_id: str, parameter: str, value: any) -> bool:
        """Update a single user field"""
        async with self.db_pool.acquire() as conn:
            try:

                query = f"UPDATE users SET {parameter} = $1 WHERE tg_id = $2"
                await conn.execute(query, value, tg_id)
                return True

            except Exception as e:
                logger.error(f"❌ Failed to update user {tg_id}: {e}")
                return False

    # async def delete(self, tg_id: str) -> bool:
    #     """Delete a user by tg_id"""
    #     async with self.db_pool.acquire() as conn:
    #         try:
    #             result = await conn.execute("DELETE FROM users WHERE tg_id = $1", tg_id)
    #             if result == "DELETE 1":
    #                 logger.info(f"🗑️ User with tg_id {tg_id} deleted.")
    #                 return True
    #             return False
    #         except Exception as e:
    #             logger.error(f"❌ Failed to delete user {tg_id}: {e}")
    #             return False

    async def get_anketas_for_user(self, user_id: int):
        async with self.db_pool.acquire() as conn:
            try:

                statement = f"""  
                    SELECT * FROM users 
                    WHERE "id" <> $1 AND "id" NOT in (
                    
                    SELECT anketa_id FROM evaluation WHERE lover_id=$1
                    UNION
                    SELECT lover_id FROM evaluation WHERE anketa_id=$1
                    
                    
                    );
                """

                records = await conn.fetch(statement, user_id)
                results = [dict(record) for record in records]

                return results
            except Exception as e:
                logger.error(f"❌ Failed to filter users: {e}")
                return False

    async def get_partners(self, user_id: int):
        async with self.db_pool.acquire() as conn:
            try:
                statement = f"""  
                    
                    SELECT * FROM users 
                    WHERE "id" in (
                    SELECT lover_id FROM evaluation
                    WHERE anketa_id=$1
                    );  
                """

                records = await conn.fetch(statement, user_id)
                results = [dict(record) for record in records]

                return results
            except Exception as e:
                logger.error(f"❌ Failed to fetch partners for user: {e}")
                return False
