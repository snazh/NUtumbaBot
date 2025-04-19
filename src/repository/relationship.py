from loguru import logger

from src.repository.schemas.relationship import RelationshipCreate
from src.repository.base import BaseRepo


class RelationshipRepository(BaseRepo):

    async def insert(self, relationship_data: RelationshipCreate) -> bool:

        async with self.db_pool.acquire() as conn:
            try:
                await conn.execute(
                    f"INSERT INTO {self.table} (user1, user2, status)"
                    "VALUES ($1, $2, $3)",
                    relationship_data.user1, relationship_data.user2, relationship_data.status
                )

                return True
            except Exception as e:
                print(e)
                logger.error(f"❌ Failed to insert relationship: ", str(e))
                return False
